# CF-001: ADR-001 Initial Compliance Check

**Report date:** 2026-04-15
**Conducted by:** Socratic Agent / Engineering Lead (@PublicEnemage)
**Scope:** `backend/app/simulation/engine/models.py`, `backend/tests/unit/test_models.py`
**Standards checked against:**
- `docs/CODING_STANDARDS.md`
- `docs/DATA_STANDARDS.md`
- `docs/adr/ADR-001-simulation-core-data-model.md`

**Status:** For Engineering Lead review. GitHub Issues not yet opened.

**Governance note:** This report was produced and reviewed by a single principal
(@PublicEnemage) during the pre-contributor governance phase documented in
`CLAUDE.md § Governance`. All dispositions marked Exception carry the required
single-principal limitation disclosure.

---

## Executive Summary

The Milestone 1 simulation core data model faithfully implements ADR-001. The
class hierarchy, interface contracts, attribute types, and module abstraction
all match the accepted ADR specification. The immutable-state contract is
correctly expressed through the abstract interface. The test suite covers all
public methods with meaningful behavioral tests.

**Findings by severity:**

| Severity | Count |
|---|---|
| Critical | 0 |
| Major | 2 |
| Minor | 6 |
| **Total** | **8** |

**Overall assessment:** Acceptable for Milestone 1. No Critical findings.
The two Major findings are anticipated consequences of the standards documents
being written after the initial code: one is a genuine ADR-vs-standard tension
requiring an exception and future ADR work; one is a missing tooling
configuration that should be remediated before Milestone 2 begins.
The Minor findings are straightforward remediations.

The ADR compliance check is clean: every class, attribute, and interface
defined in ADR-001 is implemented exactly as specified. This is the primary
criterion for Milestone 1 correctness.

---

## Findings Table

| ID | Location | Standard Violated | Severity | Proposed Disposition |
|---|---|---|---|---|
| CF-001-F01 | `models.py:95,112,134,167` | CODING_STANDARDS § Monetary Arithmetic | Major | Exception (ADR-vs-standard tension) |
| CF-001-F02 | `backend/` (absent) | CODING_STANDARDS § Ruff Configuration | Major | Remediate |
| CF-001-F03 | `models.py:15`, `test_models.py:10` | CODING_STANDARDS § Type Hints | Minor | Remediate |
| CF-001-F04 | `models.py:136,137,215` | CODING_STANDARDS § Type Hints | Minor | Remediate (with F03) |
| CF-001-F05 | `models.py:83,139,143` | CODING_STANDARDS § Docstrings | Minor | Remediate |
| CF-001-F06 | `models.py` throughout | CODING_STANDARDS § Docstrings | Minor | Defer |
| CF-001-F07 | `test_models.py:125` | CODING_STANDARDS § Naming Conventions | Minor | Remediate |
| CF-001-F08 | `test_models.py:507,551,563` | CODING_STANDARDS § Type Hints | Minor | Remediate |

---

## Detailed Findings

---

### CF-001-F01

**Severity:** Major

**Standard violated:**
> CODING_STANDARDS.md § Monetary Arithmetic: Decimal, Never float
>
> "All monetary arithmetic uses Python Decimal never float."
>
> DATA_STANDARDS.md § Units and Measurements:
> "All physical and economic measurements in the simulation are represented
> as Quantity. Never raw float, never raw Decimal without a unit."

**Location:** `backend/app/simulation/engine/models.py`
- Line 95: `initial_overrides: Dict[str, Dict[str, float]]` (ScenarioConfig)
- Line 112: `attenuation_factor: float` (PropagationRule)
- Line 134: `attributes: Dict[str, float]` (SimulationEntity)
- Line 167: `weight: float` (Relationship)

**Evidence:**

```python
# models.py:120-154
@dataclass
class SimulationEntity:
    ...
    attributes: Dict[str, float]          # current state variables
    ...
    def get_attribute(self, key: str, default: float = 0.0) -> float:
    def set_attribute(self, key: str, value: float) -> None:
    def apply_delta(self, key: str, delta: float) -> None:
```

**Severity rationale:** Major, not Critical. The finding creates a pattern
that will lead to float monetary arithmetic in simulation modules when they
read GDP, debt, and monetary quantities from `entity.get_attribute()` and
compute with the returned `float`. It does not currently produce wrong outputs
because no simulation arithmetic exists yet. However, it establishes the
foundation for every future monetary calculation. If left unaddressed before
simulation modules are written, each module will need its own remediation.

The `attenuation_factor` and `weight` fields are pure propagation weights
(dimensionless ratios in [0.0, 1.0]) and are not monetary values — float is
appropriate for them. The finding is specifically about the `attributes` dict
and `initial_overrides`, which will carry monetary quantities including GDP,
debt levels, reserve amounts, and tax revenues.

**Proposed disposition: Exception, with ADR amendment as follow-on**

This is a standards-written-after-code situation with an additional dimension:
ADR-001 explicitly specifies `attributes: Dict[str, float]`. The code conforms
to the accepted ADR. The DATA_STANDARDS document was written after ADR-001
was accepted.

**Exception rationale:** ADR-001 (accepted 2026-04-14) explicitly defines the
`attributes` field as `Dict[str, float]`. The accepted ADR specification is the
authoritative contract for Milestone 1. The DATA_STANDARDS.md `Quantity` and
`MonetaryValue` types are designed for the data ingestion and presentation
boundary, not the raw in-memory simulation state store. The attributes dict is
a performance-optimized generic store that must support rapid read/write during
event propagation across potentially hundreds of entities per timestep. Full
`Quantity` wrapping at this layer would introduce object overhead in the inner
simulation loop.

The correct remediation is not to change `models.py` to comply with the
current standard wording — it is to open a standard amendment discussion that
clarifies the boundary between: (a) the raw simulation state store, where
`float` is the correct type for simulation arithmetic, and (b) the ingestion
and presentation boundaries, where `Quantity`/`MonetaryValue` are mandatory.
This distinction is implicit in the standards but not explicit.

**Follow-on required:** Open a standard amendment issue clarifying that the
`Quantity`/`MonetaryValue` requirement applies at the data ingestion pipeline
boundary and at simulation output presentation, not at the internal simulation
state store level. The amendment should explicitly bless `Dict[str, float]`
as the correct type for the raw state attribute store and describe the
conversion points where `Quantity`/`MonetaryValue` wrapping is required.

**Risk acknowledgment:** If simulation modules compute monetary arithmetic
directly on raw `float` values from the attributes dict without Decimal
conversion — for example, summing debt service payments across entities using
float addition — rounding errors will accumulate across the simulation run.
Under the current standards, module developers are not clearly told whether
they must convert to Decimal before monetary computation or whether the
attributes dict values are already in an appropriate form for arithmetic.
This ambiguity is the actual risk. The exception is granted pending a standard
amendment that resolves the ambiguity explicitly.

**Single-principal limitation disclosure:** This exception was approved by the
same individual who holds full repository authority. No independent review is
available at this governance stage. See CLAUDE.md § Governance for the
documented plan to address this limitation.

**Exception review date:** 2026-07-15 (three months — before Milestone 2
simulation modules begin writing monetary arithmetic against the attributes dict)

---

### CF-001-F02

**Severity:** Major

**Standard violated:**
> CODING_STANDARDS.md § Linting and Formatting: Ruff
>
> "Add the following to `backend/pyproject.toml` (create if absent): [full
> Ruff configuration including ANN rules for type hints, S for security,
> B for bugbear, RET for return, SIM for simplify, TCH for type-checking]"

**Location:** `backend/` — `pyproject.toml` does not exist.

**Evidence:** `ls backend/` returns only `app/`, `Dockerfile`, `pytest.ini`,
`requirements.txt`, `tests/`. No `pyproject.toml`.

**Severity rationale:** Major. Without the specified Ruff configuration, CI
runs `ruff check .` with default rules. The default ruleset does not include
`ANN` (type annotation enforcement), `S` (security), `B` (bugbear), `RET`
(return), `SIM` (simplify), or `TCH` (type-checking). These are exactly the
rules that enforce the type hint mandate, catch common security issues, and
flag the `Optional[T]` vs `T | None` style (UP rules). The gap between
"CI passes" and "standards are enforced" is not visible to contributors.

**Proposed disposition: Remediate**

Create `backend/pyproject.toml` with the exact Ruff configuration specified in
CODING_STANDARDS.md. This also provides the correct location for mypy
configuration, which currently has no configuration file. This is a one-PR
remediation with no architectural implications.

**Target resolution date:** Before any further feature code is merged.
This should be the first PR after CF-001 review.

---

### CF-001-F03 and CF-001-F04

**Severity:** Minor

**Standard violated:**
> CODING_STANDARDS.md § Type Hints
>
> "As of Python 3.10, prefer `T | None` syntax."
>
> Implicit in the Ruff `UP` ruleset: use built-in generic types (`dict`,
> `list`) rather than `typing.Dict`, `typing.List` in Python 3.9+.

**Location:**
- `models.py` line 15: `from typing import Any, Dict, List, Optional`
- `models.py` lines 79, 95, 98, 99, 133, 134, 135, 168, 189, 192, 210, 211,
  213, 219, 221, 225, 227 — `Dict[...]` and `List[...]` usage throughout
- `test_models.py` line 10: `from typing import List`
- `test_models.py` line 498, 567 — `List[str]`, `List[Event]` usage in inline
  test class definitions

**Evidence:**

```python
# models.py:15
from typing import Any, Dict, List, Optional

# models.py:79
entity_overrides: Dict[str, ResolutionLevel] = field(default_factory=dict)

# models.py:189
propagation_rules: List[PropagationRule]
```

**Severity rationale:** Minor. Python 3.9+ supports `dict[str, ...]` and
`list[...]` as built-in generics. Python 3.10+ supports `T | None`. The
project targets Python 3.12. The legacy aliases are functionally identical
but violate the `UP` (pyupgrade) Ruff rules that CODING_STANDARDS.md requires.
No correctness impact; style and tooling impact only.

**Note:** `models.py` uses `from __future__ import annotations` (line 9) which
makes all annotations strings at runtime and permits the modern syntax even in
older Python versions. The `Optional[T]` → `T | None` migration is safe.

**Proposed disposition: Remediate (combined with CF-001-F04)**

Replace all `Dict[K, V]` → `dict[K, V]`, `List[T]` → `list[T]`,
`Optional[T]` → `T | None` throughout both files. Remove the `typing` import
in `models.py` (retaining `Any` if still needed; `Any` has no built-in
equivalent). Remove the `typing` import in `test_models.py`. This is a pure
mechanical substitution with no behavioral change. Can be done as a single
small PR.

**Target resolution date:** Combined with CF-001-F02 pyproject.toml PR, where
the Ruff `UP` rules will catch any remaining instances.

---

### CF-001-F05

**Severity:** Minor

**Standard violated:**
> CODING_STANDARDS.md § Docstrings: Google Style
>
> "The docstring answers three questions: what this does, what the parameters
> mean, and what it returns."
>
> "Every public module, class, and function has a docstring."

**Location:** `backend/app/simulation/engine/models.py`
- `ResolutionConfig.level_for` (line 81): Single-line docstring, no Args/Returns
- `SimulationEntity.get_attribute` (line 139): Single-line docstring, no Args/Returns
- `SimulationEntity.set_attribute` (line 143): Single-line docstring, no Returns
- `ScenarioConfig` class (line 87): One-line docstring with no Attributes section

**Evidence:**

```python
def level_for(self, entity_id: str) -> ResolutionLevel:
    """Return the effective resolution level for an entity."""
    return self.entity_overrides.get(entity_id, self.global_level)

def get_attribute(self, key: str, default: float = 0.0) -> float:
    """Return an attribute value, or default if not present."""
    return self.attributes.get(key, default)
```

**Severity rationale:** Minor. The one-liners communicate "what this does"
adequately for trivial methods. The CODING_STANDARDS acknowledge that a
docstring should not "restate what the code obviously does." For these
methods the code is transparent enough that a one-liner arguably satisfies the
spirit of the standard for contributors reading the code. The specific gap is
that the `default` parameter's behaviour — initializing to 0.0 if unspecified —
is not documented on `get_attribute`, and the return-on-miss behavior is
implicit in the description rather than stated in a Returns section.

**Proposed disposition: Remediate**

Expand the three method docstrings to include Args and Returns sections. For
trivial methods, these can be brief. This is a documentation-only change, no
behavioral impact.

---

### CF-001-F06

**Severity:** Minor

**Standard violated:**
> CODING_STANDARDS.md § Docstrings: Google Style
>
> Google-style dataclass documentation places attribute descriptions in an
> `Attributes:` section of the class docstring, not as inline comments on
> the field definitions.

**Location:** `backend/app/simulation/engine/models.py` — throughout all
`@dataclass` classes.

**Evidence:**

```python
@dataclass
class SimulationEntity:
    """Base for all entities in the simulation graph.
    ...
    attributes holds current simulation state variables as floats.
    metadata holds non-simulation data ...
    """
    id: str
    entity_type: str                      # 'country', 'region', 'institution'
    attributes: Dict[str, float]          # current state variables
    metadata: Dict[str, Any]             # non-simulation data
    parent_id: Optional[str] = None      # enclosing entity for hierarchical resolution
    geometry: Optional[Geometry] = None  # spatial reference, populated in Milestone 2
```

The correct Google-style form uses a structured `Attributes:` section:

```python
@dataclass
class SimulationEntity:
    """Base for all entities in the simulation graph.

    Attributes:
        id: Unique identifier. For countries, ISO 3166-1 alpha-3 code.
        entity_type: 'country', 'region', or 'institution'.
        attributes: Current simulation state variables. Keyed by variable
            name; values are floats in canonical simulation units.
        metadata: Non-simulation data (display names, ISO codes, etc.)
            that does not participate in calculations.
        parent_id: Enclosing entity ID for hierarchical resolution.
            None for top-level nation-state entities.
        geometry: Spatial reference. None until Milestone 2.
    """
```

**Severity rationale:** Minor. The inline comments communicate the same
information; this is a documentation style finding, not a correctness finding.
The information is not missing — it is in the wrong structural location.

**Proposed disposition: Defer**

Converting all dataclass inline comments to `Attributes:` sections across the
entire `models.py` file is a significant documentation refactor (six dataclass
classes) with no behavioral impact. This should be batched as part of a
documentation improvement PR rather than an isolated fix. Target: before
Milestone 2 documentation review.

**Target resolution date:** 2026-05-15 (before Milestone 2 begins)

---

### CF-001-F07

**Severity:** Minor

**Standard violated:**
> CODING_STANDARDS.md § Naming Conventions: Variables
>
> "Single-letter variables are forbidden outside comprehensions and
> mathematical proofs where convention is established."

**Location:** `backend/tests/unit/test_models.py`, line 125.

**Evidence:**

```python
def test_levels_are_ordered(self):
    levels = list(ResolutionLevel)
    values = [l.value for l in levels]   # 'l' is a single-letter variable
    assert values == sorted(values)
```

**Severity rationale:** Minor. `l` is used inside a list comprehension, which
the standard explicitly carves out as permissible ("outside comprehensions").
This may not be a violation at all — the standard says "forbidden outside
comprehensions." The `l` variable is inside a comprehension. This finding
may warrant dismissal rather than remediation.

However, `l` is also a particularly poor choice even in comprehensions because
it is visually indistinguishable from `1` (the digit one) in many fonts. The
Ruff `E741` rule flags `l`, `O`, and `I` as ambiguous variable names in all
contexts. Given that CF-001-F02 will add the Ruff `E` ruleset, this will
become a CI failure once the `pyproject.toml` is in place.

**Proposed disposition: Remediate**

Change `l` to `level` in the comprehension. One-line change. Can be included
in the CF-001-F02/F03 PR.

---

### CF-001-F08

**Severity:** Minor

**Standard violated:**
> CODING_STANDARDS.md § Type Hints
>
> "Type hints are mandatory on every function signature and every class
> attribute. No exceptions."

**Location:** `backend/tests/unit/test_models.py`
- Lines 507-509: `IncompleteModule.compute` in `TestSimulationModule`
- Lines 551-553: `QuietModule.compute`
- Lines 563-565: `TradeModule.compute`

**Evidence:**

```python
# test_models.py:507-509
class IncompleteModule(SimulationModule):
    def compute(self, entity, state, timestep) -> List[Event]:
        return []
    # entity, state, timestep have no type hints

# test_models.py:551-553
class QuietModule(SimulationModule):
    def compute(self, entity, state, timestep) -> List[Event]:
        return []
```

These inline concrete classes inside test functions implement
`SimulationModule.compute()` without parameter type hints.

**Severity rationale:** Minor. The standard applies to all function signatures
including those in test files. The risk is low — these are ephemeral test
classes that are never called through external interfaces — but the standard
makes no test-file exception, and the Ruff `ANN` rules (once the pyproject.toml
is in place from CF-001-F02) will flag these.

**Proposed disposition: Remediate**

Add type hints to the `compute` method parameters in all inline test classes.
Since these implement the `SimulationModule` abstract interface, the types are
known: `entity: SimulationEntity`, `state: SimulationState`,
`timestep: datetime`. Can be included in the CF-001-F02/F03 PR.

---

## ADR-001 Compliance Check

The following is a positive compliance record — the items the code correctly
implements from the ADR specification.

| ADR-001 Requirement | Status | Notes |
|---|---|---|
| `SimulationEntity` with id, entity_type, attributes, metadata, parent_id, geometry | ✓ Implemented | Exact match |
| `SimulationState` with timestep, resolution, entities, relationships, events, scenario_config | ✓ Implemented | Exact match |
| `Relationship` with source_id, target_id, relationship_type, weight, attributes | ✓ Implemented | Exact match |
| `Event` with event_id, source_entity_id, event_type, affected_attributes, propagation_rules, timestep_originated | ✓ Implemented | Extra `framework` and `metadata` fields added — beneficial additions, not deviations |
| `MeasurementFramework` enum with FINANCIAL, HUMAN_DEVELOPMENT, ECOLOGICAL, GOVERNANCE | ✓ Implemented | Exact match |
| `SimulationModule` abstract with `compute()` and `get_subscribed_events()` | ✓ Implemented | Exact match including return types |
| No conversion rates between MeasurementFramework values | ✓ Implemented | Architecturally enforced — distinct enum members, no conversion methods |
| Modules must not mutate SimulationState | ✓ Enforced | Documented in class docstring; unit tests verify compute() returns Events |
| ResolutionConfig with global_level and entity_overrides | ✓ Implemented | `level_for()` method added — beneficial, not a deviation |
| Event propagation via PropagationRule | ✓ Implemented | attenuation_factor and max_hops per ADR spec |

The Event class includes two fields not present in the ADR sketch:
`framework: MeasurementFramework` and `metadata: Dict[str, Any]`. Both are
beneficial additions that align with the ADR's broader principles (parallel
measurement frameworks, extensible metadata). They do not constitute deviations
from the ADR — they are reasonable elaborations of it.

---

## Recommended PR Sequence

Based on this report, the recommended remediation sequence is:

**PR 1 (immediate, before Milestone 2):**
- Create `backend/pyproject.toml` with Ruff and mypy configuration (CF-001-F02)
- Replace legacy typing imports with Python 3.10+ syntax (CF-001-F03/F04)
- Fix `l` variable in comprehension (CF-001-F07)
- Add type hints to inline test class methods (CF-001-F08)
- Expand docstrings for `level_for`, `get_attribute`, `set_attribute` (CF-001-F05)
- Title: `fix: remediate CF-001 Minor findings and add Ruff pyproject.toml`

**PR 2 (before Milestone 2, lower priority):**
- Convert dataclass inline comment documentation to `Attributes:` sections (CF-001-F06)
- Title: `docs(engine): convert dataclass attribute docs to Google-style Attributes sections`

**Issue (standard amendment, not a PR):**
- Open amendment issue for CF-001-F01 clarifying the Quantity/MonetaryValue
  boundary relative to the raw simulation state store
- Title: `STANDARD AMENDMENT: DATA_STANDARDS.md § Units and Measurements — clarify Quantity boundary at simulation state store`

---

*This report is for Engineering Lead review. GitHub Issues should be opened
after review, using the compliance finding template, one Issue per finding.*
