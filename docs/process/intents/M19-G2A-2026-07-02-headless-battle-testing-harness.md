---
name: M19-G2A-headless-battle-testing-harness
type: implementation-intent
adr: N/A — harness is a thin CLI layer over existing REST API; no new ADR required (see §1)
issues: "#1546"
status: Filed
authored-by: PM Agent
authored-date: 2026-07-02
implementing-agent: Computation Engine Agent
sprint-entry: docs/process/sprint-plans/m19-g2a-sprint-entry.md
---

# Implementation Intent: G2 Phase A — Headless Battle-Testing Harness (#1546)

## 1. Source Issue and Architecture Authority

**Issue:** #1546 — feat(harness): Mode 3 headless battle-testing harness — configurable output format, Type A/B run classification, per-run known_limitations
**ADR prerequisite:** None — confirmed CLEAR in `docs/process/sprint-plans/m19-g2a-sprint-entry.md §4`
**Authored by:** PM Agent
**Date:** 2026-07-02
**Implementing agent:** Computation Engine Agent

**Architecture authority:**
The harness calls existing REST API endpoints whose contracts are defined in `docs/schema/api_contracts.yml`:
- `POST /scenarios/{id}/advance` — steps the simulation forward; returns per-step state
- `GET /scenarios/{id}/snapshots` — retrieves state snapshots
- `GET /scenarios/{id}/measurement-output` — retrieves measurement output including cohort records, CI band, PSP

No new endpoints are introduced. The Type A / Type B run classification, the four output formats, and the `known_limitations` block are implementation decisions within the scope of this issue.

**File location decision (implementing agent):** The harness source may be placed at either:
- `backend/tests/backtesting/mode3_harness.py` (co-located with tests, simpler discovery)
- `backend/app/harness/mode3_harness.py` (proper module path, importable from test code)

The implementing agent selects the location based on Python packaging constraints. The test file path (`backend/tests/backtesting/test_m19_g2a_headless_harness.py`) is fixed regardless of harness source location.

---

## 2. Persona Trace Elements Targeted

**P-1 — Persona served:**
Primary: Ministry Analyst archetype — the quantitative analyst on a finance ministry team
(same Persona 2 family as Eleni / the Zambian ministry analyst, operating in analytical
preparation mode rather than negotiation-table reactive mode). The analyst runs backtests
during preparation to build calibration evidence, not in the 90-second negotiation window.

Secondary: Chief Methodologist — validates fidelity tier assignments and `known_limitations`
disclosures at G2B sprint entry before fixtures enter CI.

Tertiary: Persona 5 — Stakeholder Observer (Aicha, World Bank evaluation team) who will
see battle-testing evidence cited during Demo 8 Act 2 as the empirical grounding for
Bayesian CI intervals.

**P-2 — Entry state:**
The analyst has a running WorldSim instance (backend API accessible) and a scenario
that has been initialised (scenario ID known, `is_pre_calibration` set appropriately).
She has a prepared control input sequence — either historical inputs (Type A) or an
alternative policy sequence (Type B). She invokes the harness from the command line:

```
python mode3_harness.py \
  --scenario-id zmb_2012 \
  --control-inputs inputs/zmb_historical.json \
  --run-type TYPE_A \
  --format markdown
```

She receives a structured report on stdout (or redirected to file) within the expected
completion window (see P-4).

**P-3 — Journey reference:**
The harness does not map directly to a user journey step in `docs/ux/user-journeys.md`
because it is a CLI tool, not an instrument panel interaction. Its functional role is
as an analytical preparation tool that produces calibration evidence for:
- G2B: SEN and ZMB calibration fixtures fed into CI
- G3: Bayesian posterior layer (#1543) — calibrated from G2B fidelity outputs
- Demo 8 Act 2: CI intervals described as "empirically grounded" by reference to battle-testing results

The harness is infrastructure for the G2B → G3 → Demo 8 Act 2 chain.

**P-4 — Time/interaction ceiling:**
No real-time ceiling in the negotiation-table sense. Expected completion windows:
- Type A run, 12 steps, single scenario: ≤ 60 seconds on a free-tier runner (2-core, 7GB RAM)
- Type B run, 12 steps, with baseline comparison: ≤ 90 seconds
These are not hard SLA ceilings — they are design targets for the equitable build process.
If a run exceeds 120 seconds on a free-tier runner, the implementing agent documents it
in the known limitations block and the Chief Methodologist advises on step reduction.

**P-5 — Data tier requirement:**
Type A runs (backtesting against actuals) require registered historical data at minimum
Tier 2 (ESTIMATED_COMPARABLE) for the primary output attributes under evaluation.
Type B runs (counter-factual) compare against a baseline run — the data tier of the
baseline scenario governs the fidelity ceiling. DIRECTION_ONLY is the maximum fidelity
tier when any primary output attribute is Tier 3 or below.

**P-6 — Calibration evidence delivered:**
The ministry analyst can present to creditor teams: "Here is how the model performs
against the Greece 2010–12 austerity case. It correctly identifies the direction of
fiscal consolidation collapse — the DIRECTION_ONLY fidelity tier. The known limitations
are documented: stock-flow identity is not enforced, so threshold-crossing step counts
are unreliable. The CI bounds we are presenting in this analysis account for this by
treating step-count-derived estimates as Tier 3 inputs to the Bayesian posterior."

This is honest capability disclosure — the kind of transparency that builds credibility
with sophisticated counterparties who know what comparable models can and cannot do.
The ministry is not overclaiming; it is characterising its tool's limitations as precisely
as the IMF characterises its own model limitations.

**P-7 — North star capability delivered:**
At Demo 8 Act 2: Aicha (World Bank evaluation team) asks "how do we know these CI bounds
are defensible and not just a structural schedule?" The ministry team can point to the
battle-testing output: "We ran the model against seven real-world sovereign crisis cases.
On Greece 2010–12 — the most data-rich case — the model produces DIRECTION_ONLY fidelity
on primary fiscal indicators. The CI intervals you see are calibrated against this fidelity
tier via a Bayesian posterior, not assumed from a prior schedule. The limitations driving
DIRECTION_ONLY — stock-flow accounting and frozen bilateral weights — are the same
limitations listed in the `known_limitations` block of the output you can inspect."

This closes the answer with an artifact the evaluator can examine. The CI bounds are not
asserted — they are derived from documented evidence.

---

## 3. Observable Application State

### 3.1 Primary observable state — harness output

A successful harness run exits with code 0 and writes to stdout (or `--output <file>`)
a report in the selected format. The report always contains three sections:

**Section A — Run metadata:**
- `scenario_id`
- `run_type`: `TYPE_A` or `TYPE_B`
- `steps` (count executed)
- `output_timestamp` (ISO 8601 UTC)
- `is_pre_calibration` (bool — from scenario configuration)

**Section B — Per-step records (one row/record per step):**
- `step` (integer, 1-indexed)
- `fin_composite`, `hd_composite`, `eco_composite`, `gov_composite` (Decimal)
- `mda_alert_states` (list of active MDA IDs)
- `cohort_poverty_headcount` (Decimal — from `monitored_focal_cohorts[0]` if configured; null otherwise)
- `psp` (Decimal — PSP value)
- `ci_band_low`, `ci_band_high` (Decimal)
- `active_failure_modes` (list of failure mode labels)

**Section C — Summary:**
For Type A runs:
- `fidelity_tier`: one of MAGNITUDE_MATCH / DIRECTION_ONLY / STRUCTURAL_ONLY / BELOW_THRESHOLD
- `fidelity_rationale`: string — brief explanation of tier assignment
- `known_limitations`: list of strings — active gap labels from the module capability registry

For Type B runs:
- `baseline_run_id`: str
- `counterfactual_run_id`: str
- `primary_indicator`: str (e.g., `"q1_poverty_headcount_ratio"`)
- `step_differential_first_significant`: int or null — first step where diff > CI band width
- `direction_verdict`: COUNTER_FACTUAL_BETTER / BASELINE_BETTER / INDISTINGUISHABLE
- `per_step_diff`: list of Decimal
- `known_limitations`: list of strings

### 3.2 Format-specific observable states

**ASCII:** Pipe-delimited columns, fixed-width headers, human-readable in an 80-column
terminal. `known_limitations` block rendered as a plain-text list below the step table.

**CSV:** Comma-separated. Row 1 is the header row. Each subsequent row is one step record.
The `known_limitations` block is appended as a separate section below the step data,
prefixed with `# KNOWN LIMITATIONS`. Parseable by Excel/LibreOffice Calc without
post-processing (no quoted-newline values in the step rows).

**JSON:** Valid JSON per RFC 8259. Top-level keys: `run_metadata`, `per_step_records`,
`summary`. `summary.known_limitations` is a JSON array of strings. Parseable by
`json.loads()` with no preprocessing.

**Markdown:** GitHub Flavored Markdown. Per-step records as a GFM table. `known_limitations`
block as a bulleted list under a `## Known Limitations` heading. When pasted into a GitHub
issue comment, the table and list render without layout breaks.

### 3.3 Silent failure modes

**SF-1 (empty step records on exit 0):** Harness exits 0 but `per_step_records` is empty
(no steps actually executed). Detection: for any valid scenario and `--steps N` where N > 0,
assert `len(per_step_records) == N`.

**SF-2 (known_limitations absent when gaps are active):** A run exercising
`EmergencyInstrument.CAPITAL_CONTROLS` produces an empty `known_limitations` list.
Detection: run with capital controls input; assert `len(known_limitations) >= 1` and
`known_limitations` contains a string matching `"CAPITAL_CONTROLS"` or `"#1532"`.

**SF-3 (INDISTINGUISHABLE verdict when differential is clearly significant):** Type B run
with a fixture designed to produce a large differential (e.g., counterfactual removes all
fiscal consolidation, baseline maintains it) returns `INDISTINGUISHABLE`. Detection:
fixture with `|per_step_diff[i]| > ci_band_high - ci_band_low` for all i; assert
`direction_verdict != INDISTINGUISHABLE`.

**SF-4 (non-zero exit on valid input silently swallowed):** The harness encounters an
API error on a mid-run step, catches it silently, and exits 0 with a partial result.
Detection: mock the `/advance` endpoint to return 500 on step 3; assert harness exits
non-zero and writes an error to stderr.

---

## 4. Acceptance Criteria

**AC-1 (harness CLI invocable — exit 0 for valid input):**
`python mode3_harness.py --scenario-id <valid-id> --steps 3 --format ascii` exits 0 and
writes non-empty content to stdout when the scenario exists and control inputs are valid.

**AC-2 (CSV format — Excel-parseable):**
`--format csv` output passes `csv.reader()` without error; the first row is a header row;
each subsequent row contains exactly the per-step columns defined in §3.1 Section B;
no cell contains unescaped newline characters.

**AC-3 (JSON format — valid JSON with required keys):**
`--format json` output passes `json.loads()` without error; the result contains top-level
keys `run_metadata`, `per_step_records`, and `summary`; `per_step_records` is a list
of length equal to `--steps`; `summary` contains `known_limitations` as a list.

**AC-4 (Markdown format — GFM table renders):**
`--format markdown` output contains a GFM table (lines beginning with `|`); the header
row and separator row are present; `## Known Limitations` heading is present followed by
a bulleted list (even if the list is empty with a `_None_` placeholder).

**AC-5 (ASCII format — terminal-readable):**
`--format ascii` output is human-readable with column headers and at least one row of
step data visible in a standard terminal (no garbled encoding, no unformatted JSON blobs).

**AC-6 (Type A fidelity tier — Greece regression):**
A Type A run against the existing Greece 2010–12 backtesting fixture produces
`fidelity_tier: DIRECTION_ONLY` in the summary output. The pre-existing Greece backtesting
test (`backend/tests/backtesting/test_backtesting_greece.py` or equivalent) still passes
after G2A merges — regression must not be introduced.

**AC-7 (Type B direction verdict — differential fields present):**
A Type B run with a `baseline_run_id` and alternative control inputs produces a summary
containing `direction_verdict` (one of the three valid values), `step_differential_first_significant`
(int or null), and `per_step_diff` (list of Decimals, length equal to `--steps`).

**AC-8 (known_limitations — capital controls gap flagged):**
When the control input sequence includes `EmergencyInstrument.CAPITAL_CONTROLS`, the
`known_limitations` output contains at least one entry whose text references the capital
controls gap (containing `"#1532"` or `"CAPITAL_CONTROLS"` or `"Economic transmission absent"`).
This applies in all four output formats.

**AC-9 (known_limitations — stock-flow gap flagged):**
When `reserve_coverage_months` or `debt_gdp_ratio` is a primary evaluated output attribute,
`known_limitations` contains at least one entry referencing Issue #30 or the text
`"DIRECTION_ONLY at most"` or `"threshold-crossing step counts unreliable"`.

**AC-10 (known_limitations — bilateral weights gap flagged):**
When bilateral trade or debt relationships are exercised over a multi-step window (> 1 step),
`known_limitations` contains at least one entry referencing Issue #35 or the text
`"Magnitude differential may understate"` or `"bilateral weights frozen"`.

**AC-11 (non-zero exit for unknown scenario — SF-4 guard):**
`python mode3_harness.py --scenario-id nonexistent-id --format ascii` exits with a non-zero
exit code and writes an error message to stderr. Stdout contains no step data.

**AC-12 (non-zero exit for zero steps):**
`python mode3_harness.py --scenario-id <valid-id> --steps 0 --format ascii` exits with a
non-zero exit code and a meaningful error message to stderr.

**AC-13 (SF-1 guard — step count matches):**
For a valid scenario with `--steps 5`, the output contains exactly 5 per-step records
(JSON: `len(per_step_records) == 5`; CSV: 5 data rows after the header; ASCII/Markdown:
5 rows in the step table).

**AC-14 (SF-2 guard — known_limitations non-empty when capital controls active):**
Same scenario as AC-8 plus: assert `len(known_limitations) >= 1` (the list is not empty
even if no other gaps are active).

**AC-15 (SF-4 guard — mid-run API error produces non-zero exit):**
Mock the `/advance` endpoint to return HTTP 500 on the third call; assert the harness
exits non-zero and writes a message to stderr containing `"step 3"` or the error response.

---

## 5. Kryptonite Constraint Check

**Does this implementation's primary observable state require specialist mediation
for the intended user to act on it within their operational context?**

`[x]` Partial — see rationale.

**Rationale:** The harness is designed for the Ministry Analyst archetype, not for the
Finance Minister directly. The output contains technical terms (`DIRECTION_ONLY`,
`MAGNITUDE_MATCH`, `fidelity_tier`, `step_differential_first_significant`) that require
calibration literacy to interpret. This is intentional — the analyst is the target user,
not a non-specialist.

The `known_limitations` block is designed to be self-describing for a technically-literate
audience (e.g., "⚠ DIRECTION_ONLY at most — threshold-crossing step counts unreliable").
An analyst with basic modelling familiarity can interpret this without specialist translation.

**Kryptonite boundary:** The harness output is NOT intended to be read directly by Persona 2
in a 90-second negotiation window. It is analytical preparation material. The
constraint-floor search result (G1 / #1540) is the negotiation-table artifact. The harness
outputs feed Bayesian calibration (G3), which shapes the CI bounds that eventually appear
in the instrument panel in a form Persona 2 can read at the table.

No kryptonite violation exists because the harness is not positioned as a Persona 2 direct
action tool. If any Demo 8 narrative attempts to present raw harness output directly to a
non-analyst stakeholder without interpretation, the Customer Agent should flag that as a
presentation concern at the internal review stage.

---

## 6. Out of Scope (M19 G2 Phase A)

- **Streaming / real-time progress output** — harness is synchronous for M19; a streaming
  version (SSE or line-buffered stdout) is deferred to a future milestone
- **Automated parameter sweep** — G2A runs a fixed control input sequence; a sweep across
  parameter ranges requires the constraint-floor search (G1 / #1540)
- **Multi-scenario parallel execution** — G2A runs one scenario per invocation; parallelism
  across scenarios is a calling script concern (G2C will handle this via shell parallelism)
- **Web UI for harness results** — harness output is CLI/file only; rendering in the
  instrument panel is a separate future deliverable
- **Automatic calibration parameter tuning** — fidelity tier assessment is output only;
  parameter adjustment in response to fidelity results is the Chief Methodologist's manual
  step at G2B sprint entry
- **SEN and ZMB calibration fixtures** — these are G2B deliverables (#1541, #1542);
  G2A delivers the harness infrastructure those fixtures run on
- **Iceland run** — G2D (#1553); blocked by capital controls gap (#1532)

---

## 7. Test Authorship Obligation

**QA Lead:** QA Lead Agent
**Test authorship deadline:** Before any G2A implementation PR opens on `sprint/m19-g2`
**Test file location:** `backend/tests/backtesting/test_m19_g2a_headless_harness.py`

*NM-078 enforcement: test file must be placed at `backend/tests/backtesting/` — not at
`backend/tests/` root. Confirm that `pytest.ini` (or `pyproject.toml [tool.pytest.ini_options]`)
includes `backend/tests/backtesting/` in its `testpaths` or equivalent discovery configuration
before committing the test file.*

**Required test coverage:**

- **pytest — AC-1:** Call harness with a valid fixture scenario ID and `--steps 3 --format ascii`; assert exit code 0 and stdout is non-empty.
- **pytest — AC-2:** Call harness with `--format csv`; parse with `csv.reader()`; assert no parse error; assert row count = steps + 1 (header).
- **pytest — AC-3:** Call harness with `--format json`; parse with `json.loads()`; assert `run_metadata`, `per_step_records`, `summary` keys present; assert `len(per_step_records) == steps`.
- **pytest — AC-4:** Call harness with `--format markdown`; assert output contains a GFM table header (`| step |` or equivalent) and `## Known Limitations` heading.
- **pytest — AC-5:** Call harness with `--format ascii`; assert output contains column headers and at least one data row (non-JSON blob check).
- **pytest — AC-6:** Call harness with Greece 2010–12 fixture, `--run-type TYPE_A`; assert `fidelity_tier == "DIRECTION_ONLY"` in summary.
- **pytest — AC-7:** Call harness with `--run-type TYPE_B` and a baseline_run_id fixture; assert `direction_verdict` is one of the three valid values; assert `per_step_diff` length == steps.
- **pytest — AC-8 + AC-14 (SF-2 guard):** Call harness with a control input fixture containing `CAPITAL_CONTROLS`; assert `known_limitations` is non-empty and contains a string matching `CAPITAL_CONTROLS` or `#1532`.
- **pytest — AC-9:** Call harness with a run evaluating `reserve_coverage_months`; assert `known_limitations` contains a string matching `#30` or `"DIRECTION_ONLY at most"`.
- **pytest — AC-10:** Call harness with a multi-step bilateral relationship run; assert `known_limitations` contains a string matching `#35` or `"bilateral weights frozen"`.
- **pytest — AC-11:** Call harness with `--scenario-id nonexistent-id`; assert exit code != 0 and stderr contains error text.
- **pytest — AC-12:** Call harness with `--steps 0`; assert exit code != 0.
- **pytest — AC-13 (SF-1 guard):** Call harness with `--steps 5`; assert per-step record count == 5 across all four format outputs.
- **pytest — AC-15 (SF-4 guard):** Mock `POST /scenarios/{id}/advance` to return HTTP 500 on the third call; assert harness exits non-zero and stderr contains step error context.

**QA Lead acknowledgment:**
`[x]` QA Lead: Tests for AC-1 through AC-15 authored and filed. 2026-07-02
- `backend/tests/backtesting/test_m19_g2a_headless_harness.py` — AC-1 through AC-15 (all
  guard on module import from `app.harness.mode3_harness`; RED until implementation exists
  at that path; NM-078 placement confirmed in `backend/tests/backtesting/`)

---

*Intent document version: 2026-07-02. No ADR prerequisite — see sprint entry §4 for reasoning.
Sprint entry: `docs/process/sprint-plans/m19-g2a-sprint-entry.md`.
See `docs/process/agent-execution-lifecycle.md` for the five-step lifecycle this document gates.*
