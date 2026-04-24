# WorldSim Compliance Scan Registry

## Purpose

Every compliance scan is a recorded event in this registry. The registry provides:

**Auditability** — a durable record of when scans ran, what scope they covered, and
what they found. Institutional memory that survives session boundaries, contributor
changes, and the passage of time between milestones.

**Trend tracking** — findings are recorded by count and severity. Over successive scans,
the trend line shows whether the compliance posture is improving or deteriorating.
An increasing finding count across milestones is a signal that the standards are not
being applied during development, not just during reviews.

**Gap detection** — the registry makes it visible when a module or subsystem has never
been scanned. A module that appears in the codebase but never in the Scope column is a
blind spot. Gap detection is one of the primary motivations for the registry — absences
are as important as findings.

**Milestone exit gate** — a milestone exit scan must appear in this registry before a
milestone exit checklist can be signed off. The checklist references this registry
explicitly. A milestone that closes without a scan entry is a milestone that closed
without verifying its compliance posture.

---

## Scan Registry

| Scan ID | Date | Trigger | Scope | Findings Summary | Issues Created | Status |
|---|---|---|---|---|---|---|
| SCAN-001 | 2026-04-15 | Manual | ADR-001 initial implementation: `backend/app/simulation/engine/models.py`, `backend/tests/unit/test_models.py` checked against `CODING_STANDARDS.md` and `DATA_STANDARDS.md` | 2 Major (1 Exception #9, 1 Remediate #10), 5 Minor open (F03/F04 #11, F05 #12, F06 #13, F08 #14), 1 Minor resolved in PR #1 (F07) | #9, #10, #11, #12, #13, #14 | Open-findings |
| SCAN-002 | 2026-04-16 | Manual | Full architecture review: ADR-001, ADR-002, `CLAUDE.md`, `docs/scenarios/module-capability-registry.md` — all 9 Domain Intelligence Council agents in CHALLENGE mode via ARCH-REVIEW-001 | 24 blindspots: 6 immediate, 9 near-term, 8 long-term; ADR-001 and ADR-002 moved to UNDER-REVIEW; four deferred ADRs (#38–#41) opened for ADR-003 through ADR-006 | #22–#36, #38–#41 | Open-findings |
| SCAN-003 | 2026-04-17 | Manual | Full standards and policy review: `CODING_STANDARDS.md`, `DATA_STANDARDS.md`, `POLICY.md`, `CONTRIBUTING.md`, `CLAUDE.md` Domain Intelligence Council section — all 9 council agents (Track 1) and QA, Architect, Security agents (Track 2) via STD-REVIEW-001 | 32 findings: 5 CONVERGENT (SA-01–SA-05), 14 COMPATIBLE (SA-06–SA-23), 1 CONFLICT C-1 (disposed Option A — scenario tag boundary adopted; Option B deferred to #53), 2 DEPENDENCY; 10 immediate issues created; ADR-001 and ADR-002 Validity Context sections added | #42–#51, #53 | Open-findings |
| SCAN-004 | 2026-04-19 | Manual — SCR-001 implementation | Full scope: 22 files across `backend/app/` and `backend/tests/`. 5 checks: bare-except (E722), ambiguous-variable-names (E741), legacy-typing-imports, dict-str-float-attributes (QA-1 / SCR-001, new check), monetary-float-literals (warn-only). Result: **0 violations, 2 warnings** — both expected: COMPLIANCE-WARN [QA-1] `Relationship.attributes: dict[str, Any]` (ARCH-4 approved exception, SCR-001); COMPLIANCE-WARN [monetary-float] `Relationship.weight: float` (propagation coefficient, not monetary arithmetic) | None — clean scan | Clean |
| SCAN-005 | 2026-04-20 | Manual — ADR-003 M2 PostGIS foundation implementation | New files: `backend/app/db/` package (connection.py, base.py, models.py, territorial_validator.py, seed/natural_earth_loader.py), `backend/alembic/` (env.py, versions/126eb2fd0afd_initial_postgis_schema.py), `backend/tests/unit/test_territorial_validator.py`, `backend/tests/integration/test_db_seed.py`. Checks: ruff full ruleset (E, W, I, F, ANN, TCH, SIM, UP, PLR, PLW, BLE). Result: **0 violations after remediation** — 16 initial findings, all resolved (8 auto-fixed by ruff --fix; 8 manual: TCH002/TCH003 TYPE_CHECKING blocks, noqa suppressions for ANN401/TCH003 in ORM context, SIM102 restructure). Quantity wire format: value stored as str(Decimal) throughout NE loader — float prohibition enforced at DB boundary. TerritorialValidator: all 5 POLICY.md positions covered, 30/30 unit tests passing. 229 total tests passing. | None — clean scan | Clean |
| SCAN-006 | 2026-04-20 | Manual — ADR-003 M2 FastAPI layer implementation | New files: `backend/app/main.py`, `backend/app/schemas.py`, `backend/app/api/__init__.py`, `backend/app/api/deps.py`, `backend/app/api/health.py`, `backend/app/api/countries.py`, `backend/tests/unit/test_api_schemas.py`, `backend/tests/integration/test_api_endpoints.py`, `docker-compose.yml`, `backend/Dockerfile`, `.env.example`. Modified: `backend/app/db/connection.py` (lazy engine), `backend/pytest.ini` (integration mark), `backend/pyproject.toml` (mypy overrides), `.github/workflows/ci.yml` (requirements.txt in lint job). Checks: ruff full ruleset (E, W, I, F, ANN, TCH, SIM, UP, PLR, PLW, BLE). Result: **0 violations**. Float prohibition: `QuantitySchema.value` is `str`; `from_jsonb()` converts int/float/Decimal via `str(Decimal(str(v)))`. FastAPI runtime import constraint: `asyncpg.Connection` and `get_db` suppressed with `# noqa: TCH002/TCH001` (FastAPI requires runtime import for dependency injection introspection). Integration tests skip gracefully without `DATABASE_URL` — 16 collected, 16 skipped. 251 unit tests passing. | None — clean scan | Clean |
| SCAN-007 | 2026-04-21 | Manual — ADR-003 M2 MapLibre GL frontend implementation | New files: `frontend/src/types.ts`, `frontend/src/components/ChoroplethMap.tsx`, `frontend/src/components/AttributeSelector.tsx`, `frontend/src/App.tsx`, `frontend/src/App.css`. Modified: `docker-compose.yml` (frontend service added). Checks: TypeScript build (`tsc -b && vite build`). Result: **build clean, 0 TypeScript errors**. Float prohibition enforced in `types.ts`: `attribute_value: string` and `QuantitySchema.value: string` — conversion to number occurs only inside MapLibre `["to-number", ["get", "attribute_value"]]` paint expression. Territorial note display implemented: `has_territorial_note` check in hover popup renders `territorial_note` in italic when present. | None — clean scan | Clean |
| SCAN-008 | 2026-04-21 | Milestone-exit — Milestone 2 (Geospatial Foundation) exit gate | Full scope: 38 files across `backend/app/`, `backend/tests/`, `backend/alembic/`, `frontend/src/`. All code introduced or modified during Milestone 2. Checks: `scripts/compliance_scan.py --scope full` (bare-except E722, ambiguous-variable-names E741, legacy-typing-imports, dict-str-float-attributes QA-1, monetary-float warn-only). Result: **0 violations, 2 warnings** — both expected and previously accepted: COMPLIANCE-WARN [QA-1] `app/simulation/engine/models.py:230: attributes field uses dict[str, Any]` (ARCH-4 approved exception, SCR-001); COMPLIANCE-WARN [monetary-float] `app/simulation/engine/models.py:229: Relationship.weight: float` (propagation coefficient, not monetary arithmetic). Frontend TypeScript compliance: build clean (0 errors) per SCAN-007. ADR license statuses at exit: ADR-001 CURRENT, ADR-002 CURRENT, ADR-003 CURRENT. Known non-blocking defect: Issue #82 (economy_tier choropleth rendering) moved to Milestone 3. | None — clean scan | Clean |
| SCAN-009 | 2026-04-23 | Manual — ADR-004 M3 Issue #107 scenario configuration implementation | New files: `backend/alembic/versions/3a9f2c1d8e47_scenario_tables.py`, `backend/app/api/scenarios.py`, `backend/tests/unit/test_scenario_schemas.py`, `backend/tests/integration/test_scenario_api.py`. Modified: `backend/app/db/models.py` (Scenario, ScenarioScheduledInput, ScenarioStateSnapshot ORM models added), `backend/app/schemas.py` (ScenarioConfigSchema, ScheduledInputSchema, ScenarioCreateRequest, ScenarioResponse, ScenarioDetailResponse added), `backend/app/main.py` (scenarios router registered, CORS expanded to POST/DELETE). Checks: `backend/scripts/compliance_scan.py --scope full` (41 files). Result: **0 violations, 2 warnings** — both expected and pre-accepted: COMPLIANCE-WARN [QA-1] `app/simulation/engine/models.py:230` (ARCH-4 exception); COMPLIANCE-WARN [monetary-float] `app/simulation/engine/models.py:229` (propagation coefficient). 268 unit tests passing (17 new). Integration tests skip gracefully without DATABASE_URL. References Issue #61 (M3 exit checklist). | None — clean scan | Clean |
| SCAN-010 | 2026-04-23 | Manual — ADR-004 M3 Issue #111 WebScenarioRunner and state persistence implementation | New files: `backend/alembic/versions/8b2c4e6f1a3d_scenario_deleted_tombstones.py`, `backend/app/simulation/repositories/__init__.py`, `backend/app/simulation/repositories/quantity_serde.py`, `backend/app/simulation/repositories/snapshot_repository.py`, `backend/app/simulation/repositories/state_repository.py`, `backend/app/simulation/web_scenario_runner.py`, `backend/tests/unit/test_web_scenario_runner.py`, `backend/tests/integration/test_scenario_execution_api.py`. Modified: `backend/app/db/models.py` (ScenarioDeletedTombstone ORM model added), `backend/app/schemas.py` (RunSummaryResponse added), `backend/app/api/scenarios.py` (POST /run endpoint + tombstone DELETE), `backend/app/main.py` (PATCH method added to CORS). Checks: `backend/scripts/compliance_scan.py --scope full` (48 files). Result: **0 violations, 2 warnings** — both expected and pre-accepted: COMPLIANCE-WARN [QA-1] `app/simulation/engine/models.py:230` (ARCH-4 exception); COMPLIANCE-WARN [monetary-float] `app/simulation/engine/models.py:229` (propagation coefficient). 290 unit tests passing (22 new in test_web_scenario_runner.py: SA-11 determinism, SA-12 round-trip ×9, IA-1 disclosure ×2, SA-04 status transitions ×4, snapshot integrity ×2, envelope format ×4). Integration tests skip gracefully without DATABASE_URL. References Issue #111. | None — clean scan | Clean |
| SCAN-011 | 2026-04-24 | Manual — ADR-004 M3 Issue #112 Greece backtesting fixture, fidelity thresholds, CI enforcement | New files: `backend/tests/fixtures/__init__.py`, `backend/tests/fixtures/greece_2010_2012_actuals.py`, `backend/tests/fixtures/greece_2010_scenario.py`, `backend/tests/backtesting/fidelity_report.py`, `backend/tests/backtesting/test_greece_2010_2012.py`, `backend/tests/unit/test_backtesting_fixtures.py`. Modified: `backend/app/api/scenarios.py` (GET /snapshots endpoint), `backend/app/schemas.py` (SnapshotRecord added), `backend/pytest.ini` (backtesting marker added), `.github/workflows/ci.yml` (dedicated backtesting job with PostGIS service, alembic + seed + pytest -m backtesting). Checks: `scripts/compliance_scan.py --scope full` (54 files). Result: **0 violations, 2 warnings** — both pre-accepted (ARCH-4 exception; propagation coefficient). 328 unit tests passing (38 new in test_backtesting_fixtures.py). Backtesting tests skip gracefully without DATABASE_URL (4 skipped). References Issue #112. | None — clean scan | Clean |
| SCAN-012 | 2026-04-24 | Manual — ADR-004 M3 Issue #106 time acceleration controls (POST /advance, step-aware choropleth) | New files: `backend/tests/unit/test_time_controls.py`, `backend/tests/integration/test_time_controls_api.py`, `frontend/src/components/ScenarioControls.tsx`. Modified: `backend/app/schemas.py` (AdvanceResponse added), `backend/app/simulation/web_scenario_runner.py` (StepSummary dataclass + run_single_step() + _reconstruct_state_from_snapshot()), `backend/app/api/scenarios.py` (POST /scenarios/{id}/advance endpoint), `backend/app/api/countries.py` (scenario_id + step query params on choropleth, _choropleth_from_snapshot() helper), `frontend/src/types.ts` (AdvanceResponse interface), `frontend/src/components/ChoroplethMap.tsx` (scenarioId/currentStep props), `frontend/src/App.tsx` (selectedScenarioId + currentStep state, ScenarioControls render). Checks: `scripts/compliance_scan.py --scope full` (56 files). Result: **0 violations, 2 warnings** — both pre-accepted: COMPLIANCE-WARN [QA-1] `app/simulation/engine/models.py:230` (ARCH-4 exception, SCR-001); COMPLIANCE-WARN [monetary-float] `app/simulation/engine/models.py:229` (propagation coefficient). Frontend TypeScript build: clean (0 errors, `npm run build`). 337 unit tests passing (9 new in test_time_controls.py). Integration tests skip gracefully without DATABASE_URL. References Issue #106. | None — clean scan | Clean |
| SCAN-013 | 2026-04-24 | Manual — ADR-004 M3 Issue #113 comparative scenario output (compare endpoint and delta choropleth) | New files: `backend/tests/unit/test_compare_schemas.py`, `backend/tests/integration/test_compare_api.py`, `frontend/src/components/DeltaChoropleth.tsx`. Modified: `backend/app/schemas.py` (DeltaRecord + CompareResponse added), `backend/app/api/scenarios.py` (GET /scenarios/compare endpoint, _compute_delta() helper; 8-endpoint docstring update), `backend/app/api/countries.py` (GET /choropleth/{attr}/delta endpoint; 7-endpoint docstring update), `frontend/src/types.ts` (DeltaRecord + CompareResponse + DeltaChoroplethFeatureProperties interfaces), `frontend/src/App.tsx` (compareMode + secondScenarioId state, DeltaChoropleth render). Checks: `scripts/compliance_scan.py --scope full`. Result: **0 violations, 2 warnings** — both pre-accepted: COMPLIANCE-WARN [QA-1] `app/simulation/engine/models.py:230` (ARCH-4 exception, SCR-001); COMPLIANCE-WARN [monetary-float] `app/simulation/engine/models.py:229` (propagation coefficient). Frontend TypeScript build: clean (0 errors, `npm run build`). 349 unit tests passing (12 new in test_compare_schemas.py). Integration tests skip gracefully without DATABASE_URL. References Issue #113. | None — clean scan | Clean |
| SCAN-014 | 2026-04-24 | Milestone-exit — Milestone 3 (Scenario Engine) full codebase exit gate | Full scope: 59 files across `backend/app/` and `backend/tests/`. All code introduced or modified during Milestone 3. Checks: `scripts/compliance_scan.py --scope full` (bare-except E722, ambiguous-variable-names E741, legacy-typing-imports, dict-str-float-attributes QA-1, monetary-float warn-only). Result: **0 violations, 2 warnings** — both expected and pre-accepted: COMPLIANCE-WARN [QA-1] `app/simulation/engine/models.py:247` (ARCH-4 approved exception, SCR-001); COMPLIANCE-WARN [monetary-float] `app/simulation/engine/models.py:246` (propagation coefficient, not monetary arithmetic). 349 unit tests passing. ADR license statuses at exit: ADR-001 CURRENT, ADR-002 CURRENT, ADR-003 CURRENT, ADR-004 CURRENT. Open compliance exception on record: Issue #69 (IA-1 time-horizon degradation, exception documented 2026-04-24, review date M4 entry). Known architectural gap on record: Issue #139 (engine_version declaration vs. verifiable pointer, ADR-004 Known Limitation note added). References Issue #61 (M3 exit checklist). | None — clean scan | Clean |

---

## Scan Triggers

Four triggers require or may produce a compliance scan. Each produces an entry in
this registry.

### Automated (every PR — limited scope)

Every pull request triggers a machine-automated compliance check via the CI
`compliance-scan` job (`.github/workflows/ci.yml`). This scan covers
machine-detectable violations only:

- Bare `except` clauses (`E722`)
- Ambiguous variable names (`E741`)
- Legacy typing imports (`Dict`, `List`, `Optional`, `Tuple`, `Set` from `typing`)
- Float literals adjacent to monetary terminology in `backend/app/simulation/`
  (emits `COMPLIANCE-WARN`, not a build failure — requires human judgment)

Automated PR scans do not produce registry entries unless they surface a finding
that requires a compliance finding Issue. They are a preventive control, not an audit.

### Milestone-Exit (required before milestone closes)

A full-scope compliance scan covering all code introduced or modified during the
milestone. Required before the milestone exit checklist can be signed off. Scope
includes all new modules, their tests, and any changed interfaces.

A milestone-exit scan **must** appear in this registry before the exit checklist
Issue is closed. The exit checklist explicitly references the scan ID.

### Quarterly (governance audit)

A governance-level audit conducted every three months. Scope includes:

- Review of all open compliance finding Issues for expired exception review dates
- Review of all deferred findings past their target dates
- Standards review: have any rules become obsolete or counterproductive?
- Exception reconsideration: are accepted exceptions still warranted?
- Pattern analysis: are the same classes of finding recurring?

The quarterly audit produces a summary Issue documenting the current compliance posture.

### Manual (ad hoc)

Triggered by the Engineering Lead or as a consequence of a significant architecture
change (new module, major refactor, new data pipeline). Documents what was scanned,
why the scan was triggered, and what was found.

A manual scan that produces findings follows the standard compliance finding Issue
process. A clean manual scan is recorded in the registry as confirmation of the
reviewed module's compliance posture at that point in time.
