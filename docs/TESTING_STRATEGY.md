# WorldSim Testing Strategy

This document establishes the testing philosophy, current test domains, CI job
matrix, planned test domains, and test data management standards for WorldSim.

It is a companion to `CODING_STANDARDS.md` (which states what tests must cover)
and `CONTRIBUTING.md` (which states the workflow for writing them). Where those
documents say *what*, this document says *why* and *how the pieces fit together*.

---

## Philosophy

### Tests are signals, not paperwork

Every test in this repository must answer a question that matters. The question
does not have to be large — "does `apply_delta` initialize a missing key at zero
rather than raising?" is a small but real question. What is forbidden is a test
that passes trivially and tells nothing: a test that asserts a field is not None
when it can never be None, or a test that mocks the entire function under test
and asserts the mock was called.

The test suite is the primary means by which the Engineering Lead knows whether
a change broke something. If the suite is full of tests that cannot fail, it
provides a false sense of coverage. When a real defect arrives, a suite with
ten thousand empty tests is worth less than a suite with fifty meaningful ones.

### CI failures must be actionable

A CI failure that cannot be diagnosed from its output is not a failure — it is
noise. Every job in the CI pipeline is designed so that a failing step names the
violation, cites the file and line where possible, and explains why the violation
matters. A green CI run on a docs-only PR where no code changed is not
informative — it is cost without signal.

The path-based filtering described in the CI Job Matrix section exists for this
reason. Documentation commits should not spin up PostGIS services and run the
backtesting suite. A CI job that runs when it has nothing to check wastes
budget, adds latency, and dilutes the signal when a real failure arrives.

### DIRECTION_ONLY thresholds are a calibration state, not a ceiling

The Greece 2010–2012 backtesting fixture currently uses `DIRECTION_ONLY`
fidelity thresholds. This means the suite asserts that key indicators moved in
the historically correct direction (e.g., GDP contracted, unemployment rose)
without asserting that they landed within specific numeric bounds.

This is an honest description of where the engine's calibration currently stands.
The macroeconomic and demographic modules that would drive tighter fidelity are
not yet implemented. `DIRECTION_ONLY` is not the target; it is the floor we hold
while the modules that enable tighter thresholds are built.

When a module ships that directly affects a backtesting indicator, the
corresponding threshold must be tightened in the same PR. A module that ships
without tightening the threshold it enables is incomplete.

### The human cost ledger is never the first thing cut

When test coverage must be reduced under time or complexity pressure, the order
of reduction is:

1. Reduce the precision of financial fidelity assertions
2. Reduce the breadth of edge-case coverage for financial outputs
3. Reduce human cost ledger coverage — never first

A test suite that thoroughly validates GDP growth direction while leaving poverty
headcount untested has the wrong priority order. The human cost outputs are the
reason this tool exists. Their test coverage reflects that.

---

## Current Test Domains

### Unit Tests

**Location:** `backend/tests/unit/`

**Runner:** `pytest tests/unit -v`

**Speed requirement:** The full unit suite must complete in under 30 seconds.
A slow unit test is a sign that it is doing integration work — database calls,
file I/O, real HTTP, or subprocess execution. Move that logic to
`tests/integration/` or refactor the code so that the unit under test can be
exercised without those dependencies.

**Scope:** One logical unit in isolation. No database. No network. No filesystem.
No subprocess. No `sleep`. External collaborators are mocked at the boundary of
the unit under test — not inside it.

**Coverage requirements per public method:**
- At least one test for the happy path
- At least one test for each distinct error condition
- At least one test for boundary values (empty collection, zero value, maximum
  tier, missing optional field)

**What unit tests currently cover:**

| Test module | What it covers |
|---|---|
| `test_api_schemas.py` | `QuantitySchema` — Decimal-as-string serialization, `from_jsonb()` conversion, observation_date parsing, confidence_tier range |
| `test_territorial_validator.py` | `TerritorialValidator` — all five POLICY.md disputed territory positions |
| `test_compare_schemas.py` | `DeltaRecord`, `CompareResponse` — delta computation, direction classification, confidence tier propagation |
| `test_compare_step_alignment.py` | `compare_scenarios` endpoint — step alignment, 404 paths, snapshot alignment logic |
| `test_time_controls.py` | `run_single_step()` — advance endpoint, step boundary, state reconstruction |
| `test_api_endpoints.py` | FastAPI routes — health, country list, country detail, choropleth |
| `test_orchestration.py` | `WebScenarioRunner` — scenario execution, event propagation loop |
| `test_web_scenario_runner.py` | `validate_ia1_disclosure()`, state_data envelope v2, `_modules_active` field |
| `test_backtesting_fixtures.py` | Greece 2010–2012 fixture data — source citation, vintage metadata, data structure |
| `test_measurement_output.py` | `get_measurement_output()` — MultiFrameworkOutput schemas, ia1_disclosure validation, framework grouping, composite score, 404 paths |
| `test_models.py` | Core simulation data model — `SimulationEntity`, `SimulationState`, `Event`, `Quantity` |

**Mocking pattern for async endpoints:**

Unit tests for FastAPI endpoints that take an `asyncpg.Connection` parameter use
`AsyncMock` with a `fetchrow` side-effect list. Each call to `conn.fetchrow`
consumes the next item from the list. This lets tests exercise the full endpoint
logic without a live database:

```python
def _make_conn(*side_effects: dict[str, object] | None) -> AsyncMock:
    conn = AsyncMock()
    conn.fetchrow = AsyncMock(side_effect=list(side_effects))
    return conn

# Three fetchrow calls: scenario exists, snapshot at step, entity name
conn = _make_conn(
    {"scenario_id": "scen-1"},  # scenario lookup
    _snap_row(),                 # snapshot at step 1
    {"name": "Greece"},          # entity name lookup
)
```

The ordering of `side_effects` must match the ordering of `conn.fetchrow` calls
in the endpoint implementation. If the endpoint adds a new DB call, the test
mock list must be updated in the same PR.

#### Session-scoped asyncio fixtures for asyncpg

Tests that share a real asyncpg connection pool across multiple async test
functions — notably the backtesting integration tests — must declare
`loop_scope="session"` in three places. Missing any one of the three causes
`RuntimeError: Future attached to a different loop` or
`InterfaceError: cannot perform operation: another operation is in progress`.

**The three required placements:**

1. **The pool fixture in `conftest.py`** — use
   `@pytest_asyncio.fixture(scope="session", loop_scope="session")` with an
   `async` fixture body. A synchronous fixture that calls `asyncio.run()` creates
   a temporary event loop that is immediately destroyed, leaving the pool's
   connections bound to a dead loop.

2. **The client fixture that depends on the pool** — use
   `@pytest_asyncio.fixture(loop_scope="session")`.

3. **The test module's `pytestmark`** — include both markers:
   ```python
   pytestmark = [
       pytest.mark.backtesting,
       pytest.mark.asyncio(loop_scope="session"),
   ]
   ```
   With `asyncio_mode = strict` in `pytest.ini`, `pytestmark` applies the loop
   scope to every async function in the module. Individual
   `@pytest.mark.asyncio` decorators on each test function become redundant and
   can be removed.

Reference commits for the full diagnostic and fix: `6c35cab`, `89e2caa`.

---

### Integration Tests

**Location:** `backend/tests/integration/`

**Marker:** `pytest.mark.integration` (defined in `pytest.ini`)

**Runner:**
```bash
pytest tests/integration -v               # skips gracefully with exit code 5 if no DB
pytest tests/integration -v -m integration
```

**Database requirement:** Integration tests require `DATABASE_URL` to be set.
Without it, the tests are collected and then skipped (pytest exit code 5, which
the CI `test-backend` step treats as success: `|| [ $? -eq 5 ]`). This lets
`test-backend` run in CI without a PostGIS service while still exercising the
full suite locally when a database is available.

**Scope:** Interactions between the application layer and the database, between
the API and the simulation engine, or between modules that cannot be tested in
isolation. Integration tests are permitted to call the real database — that is
their purpose.

**What integration tests currently cover:**

- Database seed loader (`test_db_seed.py`) — Natural Earth data ingestion,
  entity creation, PostGIS geometry storage, territorial note population
- API endpoints with a live DB (`test_api_endpoints.py`) — choropleth data
  retrieval, country detail with real attributes
- Time controls with a live DB (`test_time_controls_api.py`) — advance endpoint
  with real scenario state transitions
- Compare endpoint with a live DB (`test_compare_api.py`) — delta computation
  across real scenario snapshots

**Requirements per integration test module:**

Each module must document which application components it exercises in its
module-level docstring. External API calls (e.g., to external data providers)
are not permitted — they must be mocked with responses recorded from real calls.
Calls to local services (test database, local Redis) are permitted.

---

### Backtesting

**Location:** `backend/tests/backtesting/`

**Marker:** `pytest.mark.backtesting` (defined in `pytest.ini`)

**Runner:**
```bash
pytest -m backtesting --tb=short -v
```

**Database requirement:** Backtesting tests require a live PostGIS database with
seeded `simulation_entities`. The GRC entity (Greece) must exist. In CI, the
`backtesting` job runs Alembic migrations and the Natural Earth loader before
executing the backtesting suite. Without `DATABASE_URL`, backtesting tests skip
with exit code 5.

**CI status:** The `backtesting` CI job is a **build gate**. A backtesting
regression is a build failure. A change that makes historical fidelity worse
must be justified, documented, and either reverted or accepted with an explicit
threshold demotion — it cannot be quietly merged.

#### The Greece 2010–2012 Fixture

The primary backtesting case is Greece 2010–2012, implemented in:
- `backend/tests/fixtures/greece_2010_2012_actuals.py` — historical actuals
- `backend/tests/fixtures/greece_2010_scenario.py` — seed configuration
- `backend/tests/backtesting/test_greece_2010_2012.py` — fidelity assertions

**Failure mode:** Coffin Corner — the operating envelope narrowed through
individually rational decisions until no policy response was available that
did not cross a binding constraint. Policy Maneuver Margin collapsed to near
zero by 2012.

**Data sources:**
- IMF WEO October 2013 (GDP, debt, current account — vintage-dated to 2010)
- World Bank WDI 2013 (unemployment, poverty, health indicators)
- EUROSTAT LFS 2010 (labour force statistics for Greece)

**Current fidelity level:** `DIRECTION_ONLY`. Assertions check that:
- GDP growth was negative (contraction) in the simulation as in the historical
  record
- Debt-to-GDP ratio increased from 2010 baseline
- The scenario does not terminate abnormally

**Threshold tightening schedule:** Unemployment direction and fiscal balance
thresholds are currently deferred — the Macroeconomic and Demographic modules
that would drive endogenous updates to these indicators are not yet implemented.
See `module-capability-registry.md`. When those modules ship, the corresponding
thresholds must be tightened in the same PR.

#### When to Tighten a Threshold

A threshold must be tightened when:

1. A domain module that directly affects the indicator ships (same PR)
2. The engine calibration for that indicator demonstrably improves
3. A new data source at a higher quality tier is registered for the indicator

A threshold must **not** be tightened in advance of the module that enables it.
Tighter thresholds on unimplemented logic produce false red builds that obscure
real regressions.

#### Planned Backtesting Cases

| Case | Failure mode | Status |
|---|---|---|
| Greece 2010–2012 | Coffin Corner | In CI (DIRECTION_ONLY) |
| Thailand 1997 | Coffin Corner + currency crisis | Planned |
| Lebanon 2019–2021 | Spin (compounding feedback) | Planned |
| Argentina 2001–2002 | Spin + currency attack | Planned |

Each new case requires a GitHub Issue using the backtesting issue template
before implementation begins. See Test Data Management below.

---

### Compliance Scan

**Location:** `backend/scripts/compliance_scan.py` + CI job steps

**CI job:** `compliance-scan` (runs after `lint` passes)

**Purpose:** Preventive control for the class of violations most likely to
produce silent wrong outputs — bare except clauses, ambiguous variable names,
legacy typing imports, and monetary float literals. This job catches machine-
detectable violations continuously rather than discovering them at milestone-exit
reviews when remediation is more expensive.

This job **complements but does not replace** the milestone-exit compliance
review recorded in `docs/compliance/scan-registry.md`. Machine-detectable
violations are a subset of compliance concerns. Semantic and architectural
compliance — correct `confidence_tier` propagation, correct `variable_type`
classification, appropriate `measurement_framework` tagging — requires human
judgment and is reviewed at milestone boundaries.

#### What the Scan Checks

**E722 — Bare except clauses** (`ruff check --select E722`)

`except:` without a named exception type is forbidden throughout the codebase.
It silently swallows signals from the runtime (KeyboardInterrupt, SystemExit)
and makes debugging impossible by hiding which exception was raised. This is the
hypoxia failure mode applied to software: the system continues executing while
impaired, with no signal that anything is wrong.

**E741 — Ambiguous variable names** (`ruff check --select E741`)

Single-character variable names `l`, `O`, and `I` are visually indistinguishable
from `1`, `0`, and `1` respectively in common monospace fonts. Forbidden.

**Legacy typing imports** (grep-based check)

`Dict`, `List`, `Optional`, `Tuple`, `Set` imported from `typing` must not
appear in `backend/app/`. Python 3.10+ built-in generics (`dict`, `list`,
`T | None`, `tuple`, `set`) are required. This keeps the codebase consistent
with the `target-version = "py312"` ruff configuration and prevents the
gradual accumulation of pre-3.10 patterns that a future maintainer would need
to untangle.

**Monetary float literals** (`scripts/compliance_scan.py --scope simulation-engine`, warn-only)

Scans `backend/app/simulation/` for `float` literals adjacent to monetary
terminology. Emits `COMPLIANCE-WARN` lines but does not fail the build —
determining whether a float is performing monetary arithmetic (a violation of
`DATA_STANDARDS.md`) or is a dimensionless propagation weight (correct) requires
human judgment that automated tooling cannot reliably supply.

Review `COMPLIANCE-WARN` output before merging. Do not merge a PR that adds
new monetary float warnings without a comment explaining why the float is not
performing monetary arithmetic.

#### Pre-Accepted Warnings

Two `COMPLIANCE-WARN` lines have been accepted as architectural exceptions and
appear in every scan run. They must not be treated as new findings:

| Location | Warning | Accepted reason |
|---|---|---|
| `app/simulation/engine/models.py` — `Relationship.attributes` | `dict[str, Any]` used for relationship attributes | ARCH-4 approved exception (SCR-001); relationship attributes hold heterogeneous metadata that cannot be typed without a plugin registry |
| `app/simulation/engine/models.py` — `Relationship.weight` | `float` propagation weight | Propagation weights are dimensionless ratios consumed by NumPy operations; they are not monetary values and are not `Quantity` instances |

Any `COMPLIANCE-WARN` line beyond these two must be reviewed and either accepted
with a documented rationale or remediated before merge.

#### Adding a New Compliance Rule

New rules follow one of two patterns depending on whether the violation is
machine-detectable:

**For ruff-detectable violations:** Add the rule code to `pyproject.toml`
`[tool.ruff.lint].select` and verify the existing codebase is clean before
merging. If existing code triggers the new rule, remediate it in the same PR or
document the exception with `# noqa: RULE — reason`.

**For violations ruff cannot detect:** Add a check to
`backend/scripts/compliance_scan.py`. The check must: name the violation
clearly, cite the file and line, and either fail the build (for hard violations)
or emit a `COMPLIANCE-WARN` line (for violations that require human judgment).
A compliance scan that fails without identifying what is wrong is not useful.

After adding a rule, record a scan entry in `docs/compliance/scan-registry.md`
confirming the rule was verified clean against the existing codebase. A rule
that was never run against the codebase it is supposed to protect is not a rule.

---

## CI Job Matrix

The CI workflow (`/.github/workflows/ci.yml`) uses a `changes` detection job
to gate downstream jobs on which file groups changed. This prevents expensive
jobs (PostGIS service spin-up, pip install, full test suite) from running on
commits that only touch documentation.

### How Path Filtering Works

A `changes` job using `dorny/paths-filter@v3` always runs first. It outputs
three boolean flags:

| Output | Filter pattern | Meaning |
|---|---|---|
| `backend` | `backend/**` | Any file under `backend/` changed |
| `frontend` | `frontend/**` | Any file under `frontend/` changed |
| `backtesting` | `backend/tests/backtesting/**`, `backend/tests/fixtures/**` | Fidelity threshold files or fixture data changed |

Downstream jobs read these outputs via `needs.changes.outputs.*` and include an
`if:` condition. The `changes` job itself always runs; it is the only cost
incurred on documentation-only commits.

### Job Trigger Matrix

| Files changed | `lint` | `test-backend` | `backtesting` (PostGIS) | `compliance-scan` |
|---|---|---|---|---|
| `docs/`, `*.md` only | skipped | skipped | skipped | skipped |
| `backend/app/` | runs | runs | skipped | runs |
| `backend/tests/unit/` or `backend/tests/integration/` | runs | runs | skipped | runs |
| `backend/tests/backtesting/` or `backend/tests/fixtures/` | runs | runs | **runs** | runs |
| `frontend/` only | runs | runs | skipped | runs |
| Mixed backend + docs | runs | runs | depends on backtesting filter | runs |

### Job Dependencies

```
changes (always runs)
  ├─► lint                  [if: backend or frontend changed]
  │     └─► compliance-scan [if: backend or frontend changed]
  └─► test-backend          [if: backend or frontend changed]
        └─► backtesting     [if: backtesting files changed]
```

`backtesting` requires `test-backend` to succeed because unit tests are a
prerequisite for the full PostGIS run. If unit tests fail, the PostGIS backtesting
suite does not run.

### Why Backtesting Has a Tighter Filter Than `test-backend`

`test-backend` runs the backtesting suite without a live database via:
```bash
pytest tests/backtesting -v || [ $? -eq 5 ]
```
Exit code 5 (no tests collected or all skipped) is treated as success. Changes
to `backend/app/` therefore get lightweight backtesting coverage for free — the
fixtures load, the test collection runs, and any import errors surface without
the PostGIS service.

The full PostGIS `backtesting` job is reserved for commits that change the files
that directly encode fidelity thresholds: the fixture data and the threshold
assertions. This is the only change type that can cause a backtesting regression,
and it is the only change type that requires the expensive job to detect it.

### ci.yml Is Not Subject to Path Filtering

Changes to `.github/workflows/ci.yml` itself always trigger the full workflow
because GitHub re-evaluates the workflow definition on every push. This is the
correct behavior — a change to the workflow definition that would skip its own
validation is not safe.

---

## Planned Test Domains

The following test domains are identified and planned. None are currently
implemented. Each stub defines scope and activation criteria so that the
Engineering Lead and future contributors have a clear target when implementation
begins.

### API Contract Testing

**Purpose:** Validate that the live FastAPI application's actual HTTP responses
conform to the OpenAPI schema it declares. Catches schema drift — the case where
a response model changes in code but the OpenAPI export used by consumers has
not been updated (or vice versa).

**Tool:** `schemathesis` (hypothesis-based OpenAPI testing) or `dredd`
(OpenAPI contract testing against a live server).

**Scope:**
- Every endpoint in `app/api/` has at least one contract test
- Schema validation covers response status codes, required fields, field types,
  and the Decimal-as-string constraint on `value`, `composite_score`,
  `floor_value`, `current_value`
- Contract tests run against a real running server instance, not a TestClient mock

**Activation criteria:** Implement when the API surface stabilizes after
Milestone 4. Priority: before first external consumer (finance ministry or
research institution) accesses the API.

---

### Frontend UI Testing

**Purpose:** Verify that the MapLibre choropleth, scenario controls, and
measurement output display work end-to-end in a real browser, including
interactions that unit tests cannot exercise (map rendering, panel toggling,
step advance flow).

**Tool:** Playwright (TypeScript, headless Chromium).

**Scenarios to cover once the scenario selector exists:**

1. **Choropleth renders with real data** — load the app, confirm the map renders
   at least one colored country, confirm the attribute selector populates.

2. **Scenario create → advance → choropleth update** — create a scenario via
   the panel, advance one step, confirm the choropleth reflects updated values.

3. **Compare mode** — create two scenarios, advance each, activate compare mode,
   confirm delta choropleth renders with the correct direction coloring.

4. **Measurement output panel** — advance a scenario with Greece (GRC) in scope,
   open the measurement output panel, confirm all four framework tabs are present,
   confirm `composite_score` fields display as strings not floats, confirm the
   IA-1 disclosure is visible.

5. **MDA alert display** — when a Minimum Descent Altitude threshold is breached
   (once the MDA checker ships in Milestone 4 Decision 3), confirm the alert
   appears in the relevant framework panel with the correct severity color.

**Activation criteria:** Implement in Milestone 4 or 5, once the scenario
selector UI is stable enough that UI test selectors will not break on every
commit.

---

### Performance Testing

**Purpose:** Establish throughput baselines before the first institutional user
load test reveals them under pressure. Performance regressions in snapshot
write throughput or choropleth query latency would directly affect usability
for a finance ministry running a scenario with a 50-entity scope.

**Scope:**

| Benchmark | Target | What breaks it |
|---|---|---|
| Snapshot write throughput | < 100ms per step for a 50-entity scenario | N+1 queries in `write_snapshot()`, unindexed joins |
| Choropleth query latency (single attribute) | < 200ms p99 | Missing spatial index, unoptimized JSONB extraction |
| Unit test suite completion | < 30 seconds | Tests that call real databases or sleep |
| `get_measurement_output` per-entity | < 50ms | Full table scan for percentile computation across entities |

**Tool:** `locust` for HTTP load testing; `pytest-benchmark` for unit-level
throughput assertions.

**Activation criteria:** Implement before the first institutional user engagement.
Establish baselines on current hardware before optimizing — premature optimization
against unmeasured baselines is the wrong order.

---

### Security Testing

**Purpose:** Automated detection of the most common vulnerability classes before
they reach production. WorldSim processes country-level economic and governance
data. A vulnerability that allows unauthorized access to scenario configurations
or simulation state could expose analytical work product to adversarial actors.

**Three layers:**

**Static analysis (SAST) — Bandit or Semgrep**

Scan `backend/app/` for: SQL injection risks in raw query construction,
hardcoded credentials, insecure deserialization, subprocess injection, and
path traversal. The asyncpg parameterized query pattern (`$1`, `$2`) is the
correct mitigation for SQL injection and must be enforced by the scanner.

Run as part of the `lint` CI job or as a separate `security-scan` job.

**Dependency vulnerability scanning — pip-audit or Safety**

Scan `backend/requirements.txt` for known CVEs. Run on every PR that modifies
`requirements.txt` and on a weekly schedule against `main` regardless of
changes. A critical CVE in a dependency is a blocker; a high CVE requires
assessment before merge.

**License scanning**

Scan production dependencies for license incompatibilities with the WorldSim
open-source license. GPL-licensed dependencies in a library that WorldSim
intends to distribute may impose viral licensing requirements. Identify before
adding, not after.

**Activation criteria:** Implement before first public release. SAST and
dependency scanning are low-cost to add to the CI pipeline and should be
prioritized in Milestone 5 infrastructure work.

---

## Test Data Management

### Backtesting Fixture Standards

Every backtesting fixture in `backend/tests/fixtures/` must satisfy these
requirements before it can be referenced by a backtesting test:

**1. Data source registration**

Every data point in the fixture must have a registered `source_id` in
`backend/app/data/source_registry.py`. The source registration must include:
the full dataset name, the specific release or vintage, the access date, the
data quality tier, and any known limitations for the country or period covered.

"World Bank" is not a source registration. `WB_WDI_GDP_GRC_2013_VINTAGE` with
a registration that cites "World Bank World Development Indicators, GDP (current
USD), Greece, 2013 vintage, accessed 2026-04-20, Tier 1" is a registration.

**2. Vintage dating**

Only data published on or before the scenario start date may be used as seed
data. A fixture seeded with 2024 World Bank data for a 2010 scenario is not
a backtesting fixture — it is a retrohindcasting exercise that uses information
unavailable at the time. Vintage dating must be verified and documented in the
fixture's module-level docstring.

Sources that do not support vintage retrieval must be documented as such, with
a note on how the vintage constraint was approximated.

**3. Fidelity threshold specification**

Each backtesting test must specify its threshold type explicitly:

| Threshold type | Meaning | When to use |
|---|---|---|
| `DIRECTION_ONLY` | Indicator moved in the correct direction | Engine calibration is early; no module drives the indicator endogenously yet |
| `WITHIN_PCT(n)` | Value within ±n% of historical at each step | Module drives the indicator; calibration is sufficient for bound checking |
| `EXACT_MATCH` | Value matches historical within floating-point tolerance | Reserved for accounting identities, not simulation outputs |

The threshold type and its justification are part of the fixture's metadata,
not just an implementation detail of the assertion.

**4. Failure mode documentation**

Each fixture documents which of the five aviation failure modes it tests:

| Failure mode | WorldSim analog | Current fixtures |
|---|---|---|
| Spin | Compounding feedback with narrow recovery window | Lebanon 2019 (planned) |
| Coffin Corner | Convergence of constraints | Greece 2010, Thailand 1997 (planned) |
| Hypoxia | Impaired judgment without awareness | Venezuela 2014 (planned) |
| Backside of power curve | Sign-inverted control response | Argentina 2001 (planned) |
| Get-there-itis | Commitment overriding situational assessment | (no case planned yet) |

**5. Historical narrative**

The fixture's module-level docstring includes a brief historical narrative:
what actually happened, what the key decisions were, and why this case
demonstrates the failure mode. This narrative is curriculum for the Socratic
Agent and reference for assessing model fidelity when the simulation diverges
from the historical record.

### Case Registration Protocol

Before any backtesting case implementation begins, a GitHub Issue must be
opened using the backtesting issue template. The issue must specify:

- The historical case name and date range
- The failure mode it exercises
- The data sources to be used (with access verification)
- The initial fidelity threshold type and the milestone at which it is expected
  to tighten
- The specific indicators to be asserted, with their sources

This registration protocol (formalized in ADR-005 Decision 5) ensures that
backtesting cases are planned with explicit exit criteria rather than
implemented opportunistically and left with indefinitely deferred thresholds.
A case with no plan for tightening its threshold is a case with no plan for
improving its coverage.

The issue must be assigned to the milestone in which the case will ship and
labeled `enhancement`. It must reference the relevant module implementation
issues so that threshold tightening is tracked alongside module development.

### Snapshot Fixture Pattern

Unit tests that exercise endpoint logic against snapshot data use the `_snap_row`
helper pattern established in `test_measurement_output.py`. The helper produces
a dict that matches the column structure of `scenario_state_snapshots`, with
`state_data` serialized as a JSON string matching the v2 envelope format:

```python
{
    "_envelope_version": "2",
    "_modules_active": [],
    "GRC": {
        "gdp_growth": {
            "_envelope_version": "1",
            "value": "-0.054",
            "unit": "dimensionless",
            "variable_type": "ratio",
            "confidence_tier": 1,
            "observation_date": None,
            "source_registry_id": "IMF_WEO_2013",
            "measurement_framework": "financial",
        }
    }
}
```

The `ia1_disclosure` field is not part of `state_data` — it is stored separately
in the snapshot row and validated by `validate_ia1_disclosure()` at write time.
The canonical value is `IA1_CANONICAL_PHRASE` from
`app.simulation.repositories.quantity_serde`.

New snapshot fixtures must use the v2 envelope format. The v1 envelope format
(no top-level `_envelope_version` key) is legacy and must not be introduced in
new test code.
