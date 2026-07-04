# DevSecOps Infra Review — CI Health: Persistent backtesting Job Failure on release/m19

**Type:** ci-health
**Date:** 2026-07-04
**Milestone:** M19 — Constraint Search and Empirical Calibration
**Authored by:** DevSecOps Agent (DS)
**Triggered by:** EL request — "DS Agent: please investigate and log this incident" (session 2026-07-04, following observation of CI failure on release/m19 during sprint/m19-g7 push attempt)
**Sources:** GitHub Actions run logs (run IDs 28710969094, 28711570146, 28711962035); `ci.yml` workflow; CM Sprint A/B/C test files; near-miss registry; known-issues registry

---

## Incident Summary

The `backtesting` CI job has been failing persistently on `release/m19` across multiple
consecutive runs. The sprint/m19-g7 push was initially blocked because a required Ruleset
check (`lint`) was in-progress on `release/m19` — the block resolved once CI completed,
revealing the persistent backtesting failures below.

**Affected CI runs (all on `release/m19`, event: `push`):**

| Run ID | Created UTC | Conclusion |
|---|---|---|
| 28710969094 | 2026-07-04 15:32 | failure |
| 28711570146 | 2026-07-04 15:54 | failure |
| 28711923210 | 2026-07-04 16:07 | failure |
| 28711962035 | 2026-07-04 16:09 | failure |

**All four required Ruleset checks pass in each run:**
`changes` ✅ · `lint` ✅ · `test-backend` ✅ · `compliance-scan` ✅

The `backtesting` job is NOT a required check in `sprint-branch-ci-gate` or
`release-branch-ci-gate`. PRs continue to auto-merge. The failure is visible in the
overall run status but does not block merges.

---

## Part 1 — Root Cause Analysis

### 1.1 Failing tests

In each run, `pytest -m backtesting --tb=short -v` (run from `cd backend`) collects
59 tests and produces 4 failures, all from CM Sprint A/B/C calibration test files:

| Test | File | Failure |
|---|---|---|
| `test_grc_counterfactual_hd_composite_magnitude_at_step_4` | `tests/test_m19_cm_a_elasticity_calibration.py` | `per_step_diff[3]` not in [0.010, 0.20] |
| `test_grc_counterfactual_per_step_diff_positive_at_step_4` | `tests/test_m19_cm_a_elasticity_calibration.py` | value non-positive |
| `test_arg_hd_composite_divergence_within_magnitude_bounds` | `tests/test_m19_cm_b_elasticity_calibration.py` | `per_step_diff[2]` not in [0.003, 0.050] |
| `test_pak_hd_composite_divergence_within_magnitude_bounds` | `tests/test_m19_cm_c_elasticity_calibration.py` | `per_step_diff[2]` not in [0.002, 0.035] |

All 55 remaining tests PASS (standard backtesting fixtures: Greece, Argentina, Ecuador,
Lebanon, Iceland, SEN, ZMB, G2A/G2C harness tests).

### 1.2 Skip guard analysis

All three CM calibration test files contain the same fixture-level skip guard:

```python
_DATABASE_URL = os.environ.get("DATABASE_URL")

@pytest_asyncio.fixture(loop_scope="session")
async def asgi_client(self) -> AsyncGenerator[httpx.AsyncClient, None]:
    if not _DATABASE_URL:
        pytest.skip(
            "DATABASE_URL not set — skipping CM Sprint A harness integration tests"
        )
```

**The guard evaluates `_DATABASE_URL != None`.** This is insufficient.

The CI `backtesting` job provides a full PostGIS service and sets:
```yaml
env:
  DATABASE_URL: postgresql://worldsim:worldsim@localhost:5432/worldsim
```

So `_DATABASE_URL` IS set. The skip guard does NOT fire. The tests run.

### 1.3 Database seeding gap

The CI `backtesting` job seeds with:
```yaml
- name: Seed Natural Earth data (creates GRC entity required by backtesting)
  run: cd backend && python -m app.db.seed.natural_earth_loader
```

`natural_earth_loader` creates entity records (country IDs, names, ISO codes). It does
NOT load:
- Economic scenario configurations (GDP growth rates, fiscal multipliers, initial state)
- Simulation run input data (the parameters GRC/ARG/PAK counter-factual runs require)
- Pre-computed hd_composite trajectory data

The CM MAGNITUDE tests run a live simulation against the API (`httpx.AsyncClient` →
`ASGITransport(app=app)`) — they require the API to return meaningful `hd_composite`
divergence between heterodox and orthodox scenario paths. With only entity records
seeded, the simulation has no economic input data and produces near-zero `hd_composite`
values across all steps. `per_step_diff[3]` ≈ 0 → magnitude bounds fail.

### 1.4 Why the `backtesting` job runs at all

The `backtesting` job condition is:
```yaml
if: needs.changes.outputs.backtesting == 'true' ||
    (github.event_name == 'workflow_dispatch' && inputs.force_backtesting == true)
```

The paths filter:
```yaml
backtesting:
  - 'backend/tests/backtesting/**'
  - 'backend/tests/fixtures/**'
```

The CM calibration test files are at `backend/tests/test_m19_cm_a/b/c_*.py` — NOT in
`backend/tests/backtesting/`. They do not trigger the `backtesting` filter directly.

**Observed trigger:** The `backtesting` job ran on all four push events. At least one
of the triggering pushes corresponds to a merge of a PR that touched
`backend/tests/backtesting/` or `backend/tests/fixtures/` (e.g., G2B SEN/ZMB fixture
integration, G2C harness integration). The `dorny/paths-filter` action for push events
compares against `github.event.before` — when multiple PRs merge rapidly or a prior
CI run was queued, the diff window may span multiple PR merges, including ones that
touched `backend/tests/backtesting/`. Once the backtesting filter fires, `pytest -m
backtesting` collects ALL tests with that mark, including the CM calibration tests in
`backend/tests/`.

**Secondary finding:** The CM calibration test files carry `@pytest.mark.backtesting`
but live in `backend/tests/` (not `backend/tests/backtesting/`). This creates a
systematic divergence between "what files trigger the backtesting job" and "what tests
the backtesting job runs." Changes to CM calibration files do NOT trigger the backtesting
job; changes to unrelated backtesting fixture files DO pull in CM calibration test
failures.

### 1.5 Relationship to open issues

The 4 failing tests are the AC-1 MAGNITUDE forward-condition tests for CM Sprint A
(GRC), CM Sprint B (ARG), and CM Sprint C (PAK). These are tracked as:

- **#1711** — Demo 8 Act 2 verification: GRC AC-1 live harness run
- **#1712** — Demo 8 Act 2 verification: ARG AC-1 live harness run
- **#1713** — Demo 8 Act 2 verification: PAK AC-1 live harness run

All three are OPEN with status "DATABASE_URL prerequisite — no code changes." The intent
was always to run these tests in a properly seeded environment, not in the CI backtesting
job. They are designed as operational verification steps, not CI gates.

---

## Part 2 — Classification

### 2.1 Known Issue vs Near-Miss determination

Per CLAUDE.md: *"If the fix requires changing our own code, process, or documents →
near-miss. If the fix requires waiting for an upstream vendor → Known Issue."*

The fix requires changing our own code (the skip guard) or process (separating MAGNITUDE
integration tests from the CI backtesting job). **This is a Near-Miss, not a Known Issue.**

The root gaps are:

1. **Skip guard scope mismatch (NM-097 — primary):** The `DATABASE_URL` guard prevents
   skipping when CI has a database but the database lacks economic data. The correct
   guard should verify data presence, not just database connectivity.

2. **Test file location mismatch (NM-097 — secondary):** CM calibration MAGNITUDE tests
   live in `backend/tests/` but carry `@pytest.mark.backtesting`. The backtesting job
   CI filter watches `backend/tests/backtesting/**`. MAGNITUDE tests are invisibly pulled
   into CI runs when unrelated fixture files change.

### 2.2 Severity

**Medium.** The `backtesting` job is not a required Ruleset check; PRs auto-merge
regardless of its result. However:

- `release/m19` has been showing "CI failure" status on every push for multiple days
- The failure misleads engineers reviewing CI health (the run looks broken when it isn't)
- If `backtesting` is ever added to a required check list, it would immediately block all
  `release/m19` merges
- The fix is straightforward and should precede Demo 8

---

## Part 3 — Recommended Process Improvements

### 3.1 Immediate fix (data-presence guard)

Add a data-presence check to the `asgi_client` fixture in all three CM calibration test
files. The check verifies that the entity has economic scenario data loaded, not just
that DATABASE_URL is set. Suggested implementation:

```python
@pytest_asyncio.fixture(loop_scope="session")
async def asgi_client(self) -> AsyncGenerator[httpx.AsyncClient, None]:
    if not _DATABASE_URL:
        pytest.skip("DATABASE_URL not set — skipping CM harness integration tests")
    # Verify GRC/ARG/PAK entity exists AND has simulation data beyond entity record
    async with get_db_session() as session:
        result = await session.execute(
            text("SELECT COUNT(*) FROM simulation_runs WHERE entity_id = :eid"),
            {"eid": ENTITY_ID}
        )
        if result.scalar_one() == 0:
            pytest.skip(
                f"No simulation runs for {ENTITY_ID} — live harness seeding required. "
                f"See issues #1711/#1712/#1713."
            )
    async with httpx.AsyncClient(...) as client:
        yield client
```

This makes the skip condition accurate: tests skip gracefully when the CI database has
entity records but no simulation data. Tests run (and are expected to pass) only in a
fully seeded environment.

### 3.2 File location clarification

Consider moving `test_m19_cm_a/b/c_elasticity_calibration.py` to
`backend/tests/backtesting/` so that the paths filter correctly triggers the backtesting
job when these files change. Currently changes to CM calibration test files do not
re-trigger the backtesting CI job, which means test file changes are not validated by
the full backtesting suite in CI.

Alternatively, expand the `backtesting` paths filter to include `backend/tests/test_m19_cm_*.py`.

### 3.3 NM filing

Both root gaps are filed as NM-097 in `docs/process/near-miss-registry.md`.

---

## Part 4 — Ruleset Health Status

**sprint-branch-ci-gate** (Node ID `RRS_lACqUmVwb3NpdG9yecc5IKi2kzgEV92A`)
Required checks: `changes`, `lint`, `test-backend`, `compliance-scan` — all passing ✅
`backtesting` NOT required — intentional (live database requirement). **Status: NOMINAL.**

**release-branch-ci-gate** — required checks per CLAUDE.md equivalent.
All required checks passing on `release/m19`. **Status: NOMINAL.**

**`backtesting` job:** FAILING persistently due to CM MAGNITUDE tests (NM-097). Not
blocking merges. **Status: DEGRADED — fix tracked NM-097.**

---

## Part 5 — Immediate Recommendations

| Priority | Action | Owner | Blocker |
|---|---|---|---|
| High | Add data-presence guard to CM calibration test fixtures | CE Agent / DS Agent | Demo 8 internal review |
| High | File NM-097 | PI Agent | — |
| Medium | Move `test_m19_cm_a/b/c_*` to `backend/tests/backtesting/` or expand filter | DS Agent | Post-G7 |
| Low | Add economic data seeding step to backtesting CI job for full MAGNITUDE test support | DS Agent | Post-M19 |
