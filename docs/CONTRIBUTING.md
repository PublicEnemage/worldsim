# Contributing to WorldSim

---

## What You Are Contributing To

A finance minister in a small, vulnerable country is sitting across a table
from an IMF negotiating team. They have limited time, limited staff, and
generational consequences riding on the decision they are about to make.

The IMF negotiating team has access to the most sophisticated scenario
analysis tools that exist. The finance minister may be working from Excel
and instinct.

WorldSim exists to close that gap.

This is not rhetoric. It is the operational purpose of every architectural
decision, every data standard, every line of code in this repository. The
quinoa farmer in Bolivia will never know this tool exists. Build it as if
he does.

**The human cost ledger is a primary output, not a feature.** The simulation
surfaces human impact alongside financial impact — lives affected, capability
losses, distributional effects by cohort. These outputs have equal visual
weight to financial indicators. They are never cut for velocity.

**The simulation is a reasoning tool, not an oracle.** Outputs are distributions,
not point estimates. Uncertainty is displayed, not hidden. The model's blindspots
are documented and visible. A contributor who overstates what the simulation
can claim — in code, in documentation, or in conversation — is working against
the mission.

**Open source is the mission, not the method.** The tool must be accessible
to the actors who most need it. Methodological transparency gives the tool
credibility — anyone can inspect, challenge, and improve the assumptions.
Proprietary analytical capability defeats the purpose entirely.

---

## Development Environment Setup

### Required Software

| Software | Minimum Version | Purpose |
|---|---|---|
| Python | 3.12.x | Backend simulation engine |
| Node.js | 20 LTS | Frontend toolchain |
| PostgreSQL | 15.x with PostGIS 3.x | Spatial database (Milestone 2+) |
| Redis | 7.x | Simulation state during active runs |
| Docker | 24.x | Local service orchestration |
| Git | 2.40.x | Version control |

### Step 1: Clone the Repository

```bash
git clone https://github.com/PublicEnemage/worldsim.git
cd worldsim
```

Create your feature branch from `develop`, not `main` (see Contribution
Workflow below):

```bash
git checkout develop
git checkout -b feat/your-feature-name
```

### Step 2: Python Environment

```bash
cd backend
python3.12 -m venv .venv
source .venv/bin/activate          # Linux/Mac
# .venv\Scripts\activate           # Windows PowerShell

pip install --upgrade pip
pip install -r requirements.txt
```

Verify the installation:

```bash
python -c "import numpy, pandas, networkx, fastapi; print('Backend dependencies OK')"
```

### Step 3: Database Setup (Milestone 2+)

PostGIS is not required for Milestone 1 (simulation engine only). Skip this
step if working on simulation logic, skip to Step 4.

```bash
# Start local services with Docker
docker compose up -d db redis

# Verify PostGIS
docker compose exec db psql -U worldsim -c "SELECT PostGIS_Version();"
```

### Step 4: Run the Test Suite

This is the verification step. If the test suite passes, your environment is
correct.

```bash
cd backend
pytest tests/unit -v
```

Expected output: all tests pass in under 30 seconds. If tests fail, stop —
do not proceed to writing code. Diagnose the environment issue first.

```bash
# Run the full suite including integration tests (requires database for Milestone 2+)
pytest tests/ -v

# Run with coverage
pytest tests/unit -v --cov=app --cov-report=term-missing
```

### Step 5: Linting and Type Checking

```bash
cd backend
ruff check app/
ruff format app/ --check          # --check reports without changing files
mypy app/
```

All three must pass cleanly before you commit.

### Step 6: Frontend Setup

```bash
cd frontend
npm install
npm run dev                        # starts development server
```

> **Docker users:** After merging a PR that changes frontend files, restart
> the frontend container to pick up the new files:
> ```bash
> docker compose restart frontend
> ```
> Vite HMR only catches edits to files it is already watching — it does not
> detect files that appeared or changed during a `git merge` or `git pull`.
> Without a restart, the browser will continue serving the pre-merge bundle.

### Step 7: Launching Claude Code

WorldSim uses Claude Code agents for AI-assisted development. When you open
a Claude Code session in this repository:

```bash
claude
```

The session reads `CLAUDE.md` automatically. The agents described there are
available to assist with architecture, implementation, testing, and review.

**Platform-specific notes:**

- **Mac:** Homebrew is the recommended package manager. `brew install postgresql@15 redis`
  for local services without Docker.
- **Linux:** Use your distribution's package manager. Ensure `libgdal-dev` and
  `libgeos-dev` are installed for PostGIS support.
- **Windows:** WSL2 with Ubuntu 22.04 LTS is the recommended environment. Native
  Windows support is not guaranteed for PostGIS tools.

---

## Understanding the Architecture Before Contributing

Before writing any code for the simulation engine, read the following in order:

1. **`CLAUDE.md`** — project mission, principles, simulation framework, and
   architecture overview. This is not optional background reading. Every
   architectural decision in this codebase is made against the principles
   stated there.

2. **`docs/adr/ADR-001-simulation-core-data-model.md`** — the foundational
   data model. If you do not understand why `SimulationModule.compute()` returns
   events rather than mutating state, you are not ready to implement a module.

3. **`docs/CODING_STANDARDS.md`** — the technical contracts every contributor
   must follow. Decimal not float. Type hints everywhere. No bare except.

4. **`docs/DATA_STANDARDS.md`** — if your contribution involves data ingestion,
   fiscal calculations, monetary arithmetic, or temporal reasoning.

### The Immutable State Contract

The most important contract in the simulation engine:

**Modules must not mutate `SimulationState` directly. All state changes are
expressed as `Event` objects returned from `compute()`. The engine applies
events to produce the next state.**

This is not a convention — it is an architectural requirement that enables:
- Deterministic replay: given the same initial state and event sequence,
  the simulation produces identical outputs
- Parallel module execution: modules that read state can run in parallel
  because none mutate it
- Backtesting integrity: every state transition is an auditable event with
  a source, a timestamp, and an effect

A contributor who cannot explain this contract and why it exists is not ready
to implement a simulation module. The Socratic Agent can test your understanding
before you write code.

### The Socratic Agent

The Socratic Agent is available to test architectural understanding:

```
Socratic Agent: TEST — immutable state contract and why it exists
Socratic Agent: TEST — MeasurementFramework and why no conversions exist between frameworks
Socratic Agent: TEACH — what was built in today's session on fiscal multipliers
```

Use it. The simulation's correctness depends on contributors genuinely
understanding the architecture, not just following patterns they've seen
before.

---

## The Agent Team Workflow

WorldSim uses Claude Code agents with defined roles. Understanding this workflow
helps you collaborate effectively with the agents and with other contributors.

### Agents and Their Roles

**Architect Agent** designs. It produces Architecture Decision Records, interface
specifications, and Mermaid diagrams. No significant feature is implemented
without an ADR. If you are planning a new simulation module or a significant
interface change, start a session asking the Architect Agent to draft the ADR.

**Implementation Agents** build to the Architect's design. They write feature
code, unit tests, and integration tests in the same commit. They do not deviate
from the ADR without flagging it.

**QA Agent** validates. It writes backtesting cases, runs the validation suite,
and reports regressions. A backtesting regression is a blocker.

**Security and Review Agent** audits dual-use concerns. Any feature that could
identify exploitable vulnerabilities rather than building defensive awareness
must go through this agent.

**Socratic Agent** teaches and tests. After a build session, it explains what
was built and why. Before a build session, it tests whether the contributor
is ready to build without introducing architectural errors.

**DevOps Agent** manages infrastructure — CI/CD, CDK, environment configuration.

### How You Interact with Agents

For new features, the workflow is:
1. Activate the Architect Agent to draft the ADR
2. Review and approve the ADR (humans approve, agents implement)
3. Activate an Implementation Agent to build to the spec
4. Activate the QA Agent to write backtesting coverage if applicable
5. Activate the Socratic Agent in TEACH mode after a complex session

For bug fixes and small improvements, the Implementation Agent workflow
suffices — no ADR required unless the fix reveals a design issue.

---

## Contribution Workflow

### Branch Naming

```
feat/short-description         # new feature
fix/short-description          # bug fix
docs/short-description         # documentation
test/short-description         # test additions
refactor/short-description     # refactoring
```

Branch from `develop`. Never branch from `main`.

### Step-by-Step

1. **Fork and clone** the repository if you are an external contributor.
   Core team members clone directly.

2. **Create a branch** from `develop`:
   ```bash
   git checkout develop && git pull origin develop
   git checkout -b feat/your-feature-name
   ```

3. **Write the ADR** if required (see CODING_STANDARDS.md for when an ADR
   is required). The Architect Agent can draft it. You approve it. No code
   before the ADR is approved for features that require one.

4. **Implement with tests**. Tests are written alongside the code, in the
   same commit — not after. A pull request that says "tests to follow" will
   not be merged.

5. **Run the full suite**:
   ```bash
   cd backend
   ruff check app/ && ruff format app/ --check && mypy app/
   pytest tests/ -v
   ```
   All must pass. Fix failures before opening a pull request.

6. **Run the backtesting suite**. A change that causes a backtesting regression
   must be justified and documented — it cannot be quietly accepted:
   ```bash
   pytest tests/backtesting/ -v
   ```

7. **Open a pull request** against `develop` (not `main`) using the PR template.
   The PR title must follow conventional commits format:
   `feat(engine): short description in imperative mood`

8. **Complete the PR template**:
   - What does this change?
   - Which ADR does it implement?
   - How does it affect the human cost ledger?
   - Which tests cover it?
   - Does the backtesting suite still pass?

9. **Respond to review**. Reviews may be from human maintainers or from
   the QA or Security agents. Address all comments before merge.

### Pull Request Title Format

```
feat(engine): implement annual timestep propagation loop
fix(macroeconomic): correct fiscal multiplier sign inversion
docs(adr): add ADR-002 PostGIS spatial data model
test(backtesting): add Greece 2010-2012 Coffin Corner case
```

---

## Standards Compliance

All contributions must comply with `CODING_STANDARDS.md` and `DATA_STANDARDS.md`.
These are architectural contracts, not preferences. Pull requests that violate
them will not be merged — not because of bureaucratic rule enforcement, but
because violations of these standards produce errors that are hard to find and
expensive to fix.

### Non-Negotiable Requirements

**Decimal, not float, for all monetary values.**
Float rounding errors accumulate across thousands of simulation steps and
produce plausible-looking wrong outputs with no warning signal. `MonetaryValue`
and `Quantity` enforce this at the type level. Do not bypass them.

**UTF-8 encoding, validated at ingestion.**
Convert at the boundary, before any processing. `errors="strict"` not
`errors="ignore"`.

**`MonetaryValue` type for all monetary quantities.**
Never raw `Decimal` or `float` for money in the simulation layer.

**`Quantity` type for all physical measurements.**
Includes population, energy, temperature, crop yield, area. Unit is not
optional metadata — it is part of the value.

**`SeasonalContext` for time-series data with seasonal character.**
Hemisphere-aware. No hardcoded Gregorian month ranges for season names.

**Fiscal year registry for fiscal calculations.**
FY2023 is not a universal date range. The registry resolves it.

**Dimensional safety enforcement.**
`UnitError` raises immediately on incompatible dimension conversion.
Never catch and suppress `UnitError`.

**ISO 3166-1 alpha-3 for all country codes.**
Everywhere. No alpha-2. No numeric. No common names in identifiers.

---

## The Human Cost Ledger Requirement

Any contribution that affects simulation outputs must include human cost
ledger outputs. This is the mission, not a feature.

If scope must be reduced under time pressure, reduce analytical sophistication
before reducing human impact visibility. A simpler model that shows human
consequences is better than a sophisticated model that hides them.

Tests for human cost ledger outputs must verify that values are meaningful —
not just that fields exist and are non-null, but that they respond correctly
to inputs. An austerity shock must increase poverty headcount. A health
spending cut must degrade health system capacity indicators. A currency
collapse must show deterioration in the human development dimension.

If you cannot write a meaningful test for the human cost ledger impact of
your change, that is a signal that either the change is not connected to
human outcomes (in which case, is it the right change?) or the human cost
model is not yet connected to the domain you are working in (in which case,
document this as a known limitation).

---

## Adding a New Data Source

1. **Register the source** in `backend/app/data/source_registry.py` with a
   complete `SourceRegistration` before writing any ingestion code. The
   `source_id` must be stable — it will appear in data lineage records.

2. **Assign a quality tier** with written rationale. "Tier 2 because this
   is derived from World Bank national accounts using published IMF methodology"
   is acceptable. "Tier 1 because it seems reliable" is not.

3. **Document known limitations** honestly. If a source is known to have
   poor coverage for small states, document it. If estimates are widely
   considered unreliable for specific countries or periods, document it.

4. **Verify vintage dating requirements.** Can this source be used for
   backtesting? Does it support retrieval of historical versions? Document
   the answer. If vintage retrieval is not supported, document the handling.

5. **Implement full DATA_STANDARDS.md compliance:**
   - UTF-8 conversion at ingestion boundary
   - ISO 8601 dates, UTC timestamps
   - CalendarService for any calendar arithmetic
   - FiscalYearRegistry for fiscal year resolution
   - SeasonalContext for seasonal data
   - Quantity type with canonical internal units
   - MonetaryValue type for monetary data
   - UnitError raises on incompatible conversions

6. **Write integration tests** for the ingestion pipeline using recorded
   fixture data from the actual source (not synthetic data). The fixture
   captures real-world edge cases including encoding issues, missing values,
   and format irregularities.

---

## Adding a New Simulation Module

1. **Write the ADR first.** No implementation without an approved ADR.
   The ADR must include: context, decision, alternatives considered,
   consequences (positive and negative), and a Mermaid diagram in
   `docs/architecture/`.

2. **Implement `SimulationModule`:**
   ```python
   class MyModule(SimulationModule):
       def compute(
           self,
           entity: SimulationEntity,
           state: SimulationState,
           timestep: datetime,
       ) -> List[Event]:
           # Read from entity and state. Never mutate them.
           # Return events expressing all state changes.
           ...

       def get_subscribed_events(self) -> List[str]:
           return ["shock", "policy_change"]  # event types this module reacts to
   ```

3. **Return Events, not mutations.** This is the contract. Modules that
   mutate `SimulationState` break deterministic replay, prevent parallel
   execution, and undermine backtesting integrity.

4. **Include human cost ledger outputs** where the module affects welfare
   outcomes. A macroeconomic module that models fiscal contraction must
   produce events tagged with `MeasurementFramework.HUMAN_DEVELOPMENT` for
   the welfare consequences, not just `MeasurementFramework.FINANCIAL` for
   the budget numbers.

5. **Write tests** covering:
   - Unit tests: module logic in isolation using minimal fixtures
   - Integration tests: module interaction with the event propagation engine
   - Human cost ledger tests: verify that welfare-affecting scenarios produce
     meaningful human cost outputs

6. **Update the diagram** in `docs/architecture/` in the same commit as the
   interface change.

---

## Adding a Historical Backtesting Case

Backtesting cases are among the highest-value contributions to WorldSim.
They validate the simulation's fidelity against documented history and surface
the gaps between model and reality that drive improvement.

Use the backtesting issue template when opening a GitHub Issue for a new case.

**Requirements for each backtesting case:**

1. **Data sources cited** with dataset name, version, and access date. "World
   Bank" is not sufficient. "World Bank World Development Indicators, GDP
   (current USD), accessed 2026-04-15, WDI release 2025/2" is sufficient.

2. **Vintage dating verified.** For each data point used to seed the scenario,
   confirm it was published on or before the scenario start date. Document
   which sources support vintage retrieval and how you verified the seed data's
   vintage.

3. **Fidelity threshold specified.** What does "this backtesting case passes"
   mean? State it numerically:
   - "GDP growth rate within ±1.5 percentage points annually"
   - "Debt-to-GDP ratio within ±5 percentage points at year 3"
   - "Currency depreciation within ±15% of historical rate"

4. **Failure mode documented.** Which of the five aviation failure modes does
   this case test?
   - Spin: Thailand 1997, Argentina 2001, Lebanon 2019
   - Coffin Corner: Greece 2010, Egypt 1986-1991
   - Hypoxia: Soviet Union 1980s, Venezuela 2014-2019
   - Backside of power curve: currency defense that accelerated collapse
   - Get-there-itis: policy commitment escalation despite deteriorating signals

5. **Historical narrative documented.** What actually happened? What were the
   key decisions and their consequences? This narrative is curriculum for the
   Socratic Agent and reference for assessing model fidelity.

---

## Testing Patterns

### Session-scoped asyncio fixtures with asyncpg

Tests that share an asyncpg connection pool across multiple async test
functions must declare `loop_scope="session"` in three places:

1. **The pool lifecycle fixture in `conftest.py`** — use
   `@pytest_asyncio.fixture(scope="session", loop_scope="session")` and
   make the fixture `async`. Using `asyncio.run()` in a sync fixture creates
   a temporary event loop that is immediately closed after pool creation,
   leaving every pool connection bound to a dead loop.

2. **The client fixture that uses the pool** — use
   `@pytest_asyncio.fixture(loop_scope="session")`.

3. **The test module's `pytestmark`** — include
   `pytest.mark.asyncio(loop_scope="session")` to apply session-loop scope
   to every async test function in the module:
   ```python
   pytestmark = [pytest.mark.backtesting, pytest.mark.asyncio(loop_scope="session")]
   ```
   Individual `@pytest.mark.asyncio` decorators on each test function are
   then redundant and can be removed — `pytestmark` covers them in strict mode.

If any of the three is missing, asyncpg will raise
`RuntimeError: Future attached to a different loop` or
`InterfaceError: cannot perform operation: another operation is in progress`
because pool connections are bound to the event loop in which they were created.
See commits `6c35cab` and `89e2caa` for the full diagnostic and fix record.

---

## Multilingual Contributions

Translation contributions are critically important to the mission. A tool that
exists to serve a finance minister in Bolivia is less useful if it is only
accessible in English.

**Translation keys live in** `frontend/src/i18n/locales/`. Each locale is a
JSON file keyed by translation key. English (`en.json`) is the canonical
source of truth. All translation files must have keys matching `en.json`.

**To add a new language:**
1. Create `frontend/src/i18n/locales/[language-code].json`
2. Translate all keys from `en.json`
3. Open a pull request with the completed translation
4. Request review from a native speaker with economic/political domain knowledge

**Domain knowledge is required.** Economic and political terminology —
"current account deficit," "fiscal multiplier," "sovereign debt restructuring,"
"Coffin Corner" — does not translate by language fluency alone. Translations
reviewed by a native speaker without domain knowledge may be fluent but
technically misleading. Request domain-knowledgeable reviewers explicitly.

**Simulation reproducibility note:** Translation is a presentation-layer
concern. Translation keys in the simulation layer, translated strings only
at the presentation boundary. See DATA_STANDARDS.md.

---

## Code of Conduct

WorldSim exists to level an asymmetric playing field. Contributors are expected
to engage with that mission seriously.

**Intellectual honesty is a requirement, not a preference.**

- Document model limitations. Do not omit limitations because they make the
  tool look less capable. A user who does not know the model's blindspots
  cannot apply appropriate judgment.
- When backtesting shows poor fidelity, document it. The history of
  development economics is full of models that were more confident than they
  were accurate. WorldSim explicitly does not repeat that mistake.
- The simulation is a structured reasoning tool. Contributors who represent
  it as a prediction engine in documentation, communications, or the user
  interface are violating the mission.

**Scope reduction under pressure reduces analytical sophistication first.**
When facing scope constraints, the order of reduction is:
1. Reduce model sophistication (simpler equations, fewer variables)
2. Reduce coverage (fewer countries, shorter time range)
3. Reduce human cost ledger detail

Human cost ledger outputs are never the first thing cut. They are the mission.

**Engagement with the dual-use concern is required.** The Financial Warfare
Module models attack surface identification as a tool for defense. Features
that shift the tool toward identifying exploitable vulnerabilities in specific
actors — rather than building defensive awareness — must be surfaced and
reviewed, not quietly implemented.

**Disagreement with a standard or an architectural decision is resolved
through the ADR process, not through ignoring it.** If you believe a decision
in DATA_STANDARDS.md is wrong, open an issue and make the argument. If the
argument is sound, the standard changes. If it is not sound, you have the
rationale for the current decision documented in the response.

---

## Common Development Issues

### Scenarios panel shows error / API returns 500 on `/api/v1/scenarios`

**Symptom:** Clicking the Scenarios panel arrow in the browser shows an error
message. Directly calling `curl http://localhost:8000/api/v1/scenarios` returns
`Internal Server Error`. API logs show:

```
asyncpg.exceptions.UndefinedTableError: relation "scenarios" does not exist
```

**Cause:** The database schema is missing one or more Alembic migrations.
Docker Compose starts the API container with `uvicorn` directly — it does not
run `alembic upgrade head` on startup. If you started the containers against
an existing database that predates the M3 scenario tables, or if a new
migration was merged after your containers were last built, the `scenarios`,
`scenario_state_snapshots`, and `scenario_deleted_tombstones` tables will not
exist.

**Fix:**

```bash
docker compose exec api alembic upgrade head
```

Then verify:

```bash
curl http://localhost:8000/api/v1/scenarios
# Should return [] (empty list), not an error
```

**When this recurs:** Run `alembic upgrade head` any time you pull a commit
that includes a new file under `backend/alembic/versions/`. You can check
which migrations are pending without applying them:

```bash
docker compose exec api alembic current    # shows current DB revision
docker compose exec api alembic history    # shows full migration chain
```

---

### Frontend does not reflect latest code after `git pull`

**Symptom:** You pulled new frontend changes but the browser still shows the
old UI. Hard-refreshing does not help.

**Cause:** Vite's Hot Module Replacement only watches files it was already
serving when the container started. Files added or changed by `git pull` are
not picked up automatically.

**Fix:**

```bash
docker compose restart frontend
```

---

### Natural Earth loader not run — choropleth is empty or GRC entity missing

**Symptom:** The choropleth map is blank, or a backtesting run fails with
`EntityNotFound: GRC`. The `simulation_entities` table is empty.

**Cause:** The Natural Earth boundary loader seed script has not been run
against this database.

**Fix:**

```bash
docker compose exec api python scripts/natural_earth_loader.py
```

The loader is idempotent — safe to run multiple times.

---

## Getting Help

**GitHub Issues** — bugs and feature requests, using the provided templates.
A good issue contains: what you expected to happen, what actually happened,
the minimal reproduction case, and which component is involved.

**The Socratic Agent** — for architectural questions. If you are uncertain
whether your design aligns with the simulation architecture, activate the
Socratic Agent in TEST mode before building. It is cheaper to catch a design
misalignment before implementing than after.

```
Socratic Agent: TEST — [describe what you are about to build and why]
```

**GitHub Discussions** — for design questions that are not yet specific enough
to be issues. If you are considering an approach and want input before committing
to it, Discussions is the right place.

**Pull Request Review** — the primary mechanism for feedback on contributions
in progress. Open a draft pull request early to get architectural feedback
before a full implementation is complete.
