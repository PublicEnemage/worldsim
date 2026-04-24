# ARCH-REVIEW-003: Full Council Architecture Review — Milestone 3

**Review type:** Full — all Domain Intelligence Council members, CHALLENGE mode
**Scope:** ADR-001, ADR-002, ADR-003, ADR-004, CLAUDE.md,
`docs/scenarios/module-capability-registry.md`, all files in `docs/adr/`,
and all M3 additions: `WebScenarioRunner`, scenario configuration tables,
Greece 2010–2012 backtesting fixture, time acceleration controls,
comparative scenario output, and tombstone design
**Facilitated by:** Architecture Review Facilitator
**Date:** 2026-04-24
**Status:** Complete — GitHub Issues created for all Immediate and Near-Term findings

---

## Executive Summary

Milestone 3 delivered substantial execution infrastructure: `WebScenarioRunner`
as an async scenario executor, three new database tables (`scenarios`,
`scenario_state_snapshots`, `scenario_deleted_tombstones`), a four-endpoint
scenario API, the Greece 2010–2012 backtesting fixture, `POST /advance` time
acceleration, comparative scenario output (`GET /compare`,
`GET /choropleth/{attribute}/delta`, `DeltaChoropleth.tsx`), and the tombstone
design for deleted scenario reconstruction. All four ADRs are CURRENT. CI
passes all 59 files at SCAN-014. The compliance posture is clean.

The council review has a dominant structural finding: **the M3 scenario engine
is functional as a financial simulation instrument but is architecturally
unprepared to serve as the scaffolding for Milestone 4's Human Cost Ledger.**
Three specific gaps drive this finding.

First, the `ia1_disclosure` NOT NULL enforcement — introduced as the primary
compliance control for the IA-1 acknowledged limitation — is a syntactic
constraint, not a semantic one. The DB enforces that a disclosure string is
present; it does not enforce that the string is meaningful, complete, or
accurate. An empty string, a single space, or a copy-pasted template satisfies
the NOT NULL constraint while providing zero informational value to users who
need to understand projection confidence limitations. As the Human Cost Ledger
milestone introduces longer projection horizons (multi-decade intergenerational
analysis), ia1_disclosure content becomes the primary user-facing signal about
output reliability. A NOT NULL constraint cannot carry that load.

Second, `WebScenarioRunner` in M3 executes scenarios against an empty module
list — there are no domain modules (Macroeconomic, Trade, Climate, Demographic)
implemented. The scenario engine applies `ControlInput` shocks and propagates
them through static relationship weights. The outputs look like simulation
results: numbered snapshots, JSONB state data, confidence tiers, envelope
versions. They are not. They are first-round manual-input propagation with no
endogenous dynamics, no module responses, no feedback loops. Milestone 4 will
introduce domain modules that generate endogenous events. When those modules
are wired into `WebScenarioRunner`, they will produce outputs qualitatively
different from M3 outputs — yet the M3 output schema, snapshot table, and
comparison API have no field to signal whether a snapshot includes domain module
contributions. A user comparing an M3 snapshot (no modules) to an M4 snapshot
(with Demographic module active) against the same scenario configuration has no
architectural signal that these are not comparable.

Third, the tombstone design captures `configuration JSONB` and
`scheduled_inputs JSONB` before deleting a scenario. Under the SA-11
determinism guarantee, this is sufficient to reconstruct the scenario output
given the same engine version. But it is not sufficient. The guarantee requires
three things: same configuration, same scheduled inputs, and same engine
version. The entity state that the scenario ran against — the actual attribute
values in `simulation_entities` at the time of scenario creation — is not in
the tombstone. If the Natural Earth loader is re-run after tombstone creation
and updates entity attributes, reconstruction from the tombstone will start
from a different baseline. The tombstone preserves the inputs; it does not
preserve the world those inputs operated on.

The council also notes genuine progress since ARCH-REVIEW-002: unemployment
was added to the Greece backtesting fidelity thresholds (partially addressing
BI2-I-02), the Greece fixture now runs 3 steps rather than 2 (reducing the
false-positive rate documented in BI2-I-03 / Finding 24 of ARCH-REVIEW-002),
and the `DeltaChoropleth` diverging color scale is the correct visual form for
comparative scenario analysis. These are improvements. They do not resolve the
structural gaps above.

**Key tensions identified by the council:**

- The Chief Methodologist and the Investment Agent (RISK-TOLERANT) disagree on
  the engine_version declaration gap (Issue #139). The Chief Methodologist
  holds that the SA-11 determinism guarantee is void until engine_version is a
  verifiable pointer, not a string declaration; a guarantee whose conditions
  cannot be verified is not a guarantee. The Investment Agent argues that the
  conservative block-on-mismatch posture (Issue #139, M4 resolution) is a
  sufficient compensating control: if two scenarios have different engine_version
  strings, comparison is blocked regardless of whether the string accurately
  reflects the underlying code. The gap is between formal verifiability and
  operational safety — a question of risk appetite, not architecture.
- The Development Economist and the Investment Agent (RISK-AVERSE) disagree on
  the urgency of HCL module readiness. The Development Economist holds that
  adding a Demographic module to `WebScenarioRunner` after the current snapshot
  schema is in production constitutes a retrofit that will produce backward-
  incompatible snapshot interpretation; the schema change should happen before
  M4 outputs are committed to the DB. The Investment Agent holds that the
  `_envelope_version` field in snapshots is precisely the mechanism for managing
  this evolution, and that blocking M4 module implementation pending a schema
  change would delay the mission-critical Human Cost Ledger.
- The Intergenerational Advocate and the Community Resilience Agent agree
  that ia1_disclosure semantic validation is the most important unaddressed gap
  from the IA-1 acknowledged limitation. Both note that the compliance exception
  record in Issue #69 documents the gap but the documentation does not reach
  users of the API or the frontend. The documentation is in the compliance
  system; the users are on the other side of an HTTP endpoint. The gap between
  them is the gap the council most urgently recommends bridging.

The council identified **22 distinct blindspots**: 7 immediate, 10 near-term,
and 5 long-term. GitHub Issues have been created for all immediate and near-term
findings.

---

## Findings by Agent

---

### Development Economist Agent — CHALLENGE

**Finding 1: WebScenarioRunner produces no human cost ledger outputs — M4
retrofit risk.**

`WebScenarioRunner` writes snapshots to `scenario_state_snapshots` as JSONB
state data with `_envelope_version: "1"`. In M3, that JSONB contains whatever
entity attributes exist in `simulation_entities` — which are the Natural Earth
Level 1 attributes (GDP, population, trade indices) plus any ControlInput-
propagated changes. There are no human development attributes (unemployment,
infant mortality, health system capacity, educational attainment) in the
simulation entity store. Snapshots therefore contain no human cost ledger data
by construction.

When the Milestone 4 Demographic module is implemented and wired into
`WebScenarioRunner`, it will generate endogenous events that update human
development attributes. Those attributes will appear in subsequent snapshots.
The `SnapshotResponse` Pydantic schema returns the full `state_data` JSONB —
there is no structured field distinguishing "financial indicators" from "human
cost indicators." A frontend or API consumer cannot determine from the snapshot
structure alone whether a given snapshot includes human cost data or not. When
M4 outputs exist alongside M3 outputs in the same `scenario_state_snapshots`
table, mixed-framework comparison becomes the default behavior with no
architectural safeguard against it.

The minimum required before M4 module implementation: either a
`modules_active: list[str]` field on `SnapshotResponse` recording which modules
contributed to each snapshot, or a `_modules_version` envelope metadata key
alongside `_envelope_version`. Without this, M3 and M4 snapshots are
structurally indistinguishable.

**Finding 2: ia1_disclosure is syntactically enforced but semantically void.**

ADR-004 Decision 1 specifies `ia1_disclosure NOT NULL` at the DB level as the
primary compliance mechanism for the IA-1 acknowledged limitation on confidence
tier degradation with projection horizon. The constraint is implemented. But
`NOT NULL` enforces the presence of a string — not its truth, completeness, or
adequacy as a disclosure. The Greece 2010–2012 backtesting fixture has a 3-step
projection horizon (2010→2012). The IA-1 limitation becomes consequential when
scenarios project 5, 10, or 20 years forward — exactly the timescales relevant
to the Human Cost Ledger's multi-decade analysis of intergenerational effects.

At those timescales, a `confidence_tier = 2` output carrying a boilerplate
`ia1_disclosure` string (or even an empty string — NOT NULL allows `''`) tells
users nothing about whether confidence tiers are degraded by projection distance.
Since Issue #69 (the compliance exception) defers time-horizon confidence
degradation to Milestone 4, every M3 projection carries its input data's
confidence tier with no projection-distance discount. The disclosure mechanism
exists to surface this to users. The NOT NULL constraint cannot enforce that it
does.

**Finding 3: No architecture path for human development indicators in initial
state — ARCH-REVIEW-002 BI2-I-01 carried forward.**

ARCH-REVIEW-002 Finding 1 identified that the Greece initial state contains no
human development indicators. The M3 implementation seeded the Greece fixture
from IMF WEO data (GDP growth, debt/GDP) and added unemployment as a DIRECTION_
ONLY threshold. But the `simulation_entities.attributes` JSONB for GRC still
contains no WDI-sourced or WHO-sourced human development attributes. World Bank
WDI 2010 unemployment data (12.7%), healthcare expenditure as % of GDP (9.8%),
net enrollment ratio, and infant mortality rate are all publicly available and
historiclaly documented for Greece 2010. They are not in the fixture. The
unemployment threshold tests direction; it tests the direction of a value that
must have been injected as a `ControlInput` effect, because there is no initial
unemployment stock in the entity store to trend from.

This is not a documentation gap. It is an architectural gap: the scenario
cannot produce a meaningful human cost ledger for Greece 2010–2012 because the
initial human conditions are unseeded.

---

### Political Economist Agent — CHALLENGE

**Finding 4: ia1_disclosure compliance exception approved without independent
review — governance gap compounds ia1 gap.**

The CLAUDE.md §Governance section specifies that compliance exceptions approved
during the single-principal phase must include the verbatim statement
acknowledging self-approval. Issue #69's exception record includes this
statement. But the consequence deserves more architectural attention: the IA-1
limitation is not a minor data quality concern. It means that a scenario
projecting 10 years forward carries the same `confidence_tier` as a scenario
projecting 1 year forward — potentially tier 1 or tier 2, implying high
confidence in a decade-long projection built on annual IMF data. The exception
was self-approved. The mechanism intended to surface this to users (NOT NULL)
does not surface it. The governance gap and the technical gap compound.

In Milestone 4's Human Cost Ledger context, this will produce decade-long
projections of intergenerational capability loss carrying tier 1 confidence
tags on a model with no Demographic module and no calibrated multipliers. A
finance minister reading those outputs may not know that "confidence_tier = 2"
for a 10-year projection means "this was a high-quality 2010 data point; the
10-year model projection is entirely uncalibrated."

**Finding 5: Scenario configuration has no political legitimacy initial
state — ARCH-REVIEW-002 BI2-N-02 carried forward.**

The `scenarios` table carries `modules_config` (module activation) and
`initial_overrides` (attribute value overrides). The `initial_overrides` field
allows overriding entity attribute values at scenario start. But it cannot
encode structured political context — electoral calendar, coalition fragility,
government approval rating, opposition strength. These are preconditions for
all ControlInputs: a `FiscalPolicyInput` specifying 8% of GDP spending cuts
fires identically in a country with a 70% approval majority government and a
country on the verge of a no-confidence vote. M3 does not change this.

The Milestone 4 Human Cost Ledger will surface cohort-level distributional
effects. Without political legitimacy as a state variable, the simulation will
model the distributional effects of policies that in historical reality were
politically constrained or reversed — producing an optimistic picture of
policy transmission that does not match the Human Cost Ledger's empirical
purpose.

---

### Ecological Economist Agent — CHALLENGE

**Finding 6: Tombstone preserves financial scenario configuration — ecological
future is seeded from the same absent baseline.**

The `scenario_deleted_tombstones` table captures `configuration JSONB` and
`scheduled_inputs JSONB`. In M3, `configuration` contains modules_config and
initial_overrides — both financial. Ecological initial conditions (agricultural
productivity, water stress, carbon trajectory, deforestation rate) do not exist
in `simulation_entities.attributes`, so they cannot appear in initial_overrides.
The tombstone faithfully records what was configured; it cannot record what
was never there.

When the Climate module is implemented in a future milestone, ecological
scenarios will require ecological initial conditions in entity attributes and
in scenario initial_overrides. At that point, tombstones of M3-era scenarios
will be structurally incomplete as reconstruction guides — they will specify
the financial configuration but not the ecological baseline from which the
scenario ran. The tombstone design is sound for what exists; its scope
limitation is inherited from the entity attribute gap, not from the tombstone
design itself. Both the tombstone design and the entity seeding gap must be
addressed together.

**Finding 7: DeltaChoropleth color scale is relative, not absolute —
ecological threshold crossings are visually indistinguishable.**

`DeltaChoropleth.tsx` uses percentile-based step computation for positive and
negative delta halves separately. The color assigned to a delta value is
relative to the distribution of all other delta values in that specific
comparison, not relative to any absolute scale or threshold. A delta of
-2% agricultural productivity looks the same red as a delta of -50%
agricultural productivity if both are in the most-negative percentile of their
respective comparison set.

For ecological analysis, the relevant comparison is not "how does this delta
compare to other countries in this scenario comparison" but "has this delta
crossed a threshold that implies irreversible ecosystem degradation." The
DeltaChoropleth architecture cannot represent this. A country crossing an
ecological tipping point looks visually identical to a country experiencing
a large-but-reversible productivity fluctuation. CLAUDE.md specifies
"Minimum Descent Altitudes" — hard floors with qualitatively different status
below them. The delta visualization has no mechanism for marking these floors.

---

### Geopolitical and Security Analyst Agent — CHALLENGE

**Finding 8: Engine_version declaration cannot verify SA-11 determinism —
scenario reproducibility claim is unverifiable.**

ADR-004 Knowledge Limitation (Issue #139) documents that `engine_version` is a
semantic version string, not a verifiable pointer. Two scenarios created with
`engine_version: "0.3.0"` are asserted to produce identical outputs from the
same configuration + scheduled_inputs. But two commits within the 0.3.0 release
could produce different propagation results if any simulation logic was modified
between them. A scenario created on commit `6c35cab` with engine_version
`"0.3.0"` and a scenario created on commit `89e2caa` with engine_version
`"0.3.0"` are not guaranteed identical under SA-11 because the version string
does not distinguish the commits.

The ADR-004 posture — block unconditionally on version mismatch — is a
compensating control: it prevents cross-version comparisons when the version
string differs. But it cannot prevent within-version result divergence when the
string is the same but the commit differs. For geopolitical analysis, where
scenario comparisons may inform decisions about sanctions, capital controls, or
debt restructuring, the reproducibility guarantee is a high-stakes claim. It
should be made with a verifiable mechanism (git commit hash in
`engine_version_hash` alongside the semver string) or qualified explicitly.

**Finding 9: Comparative output has no threshold-crossing markers —
ARCH-REVIEW-002 BI2-N-06 carried forward.**

`DeltaRecord` returns `delta = Decimal`, `direction = str`, and
`confidence_tier = int`. For geopolitical and security analysis, the relevant
question remains whether the delta crosses a known threshold — reserves falling
below 3 months of import coverage, debt/GDP crossing 90%, unemployment exceeding
25%. The same delta of -0.5% on `reserve_months_import_coverage` means
strategically opposite things at 6 months vs. at 3.5 months.

The `GET /choropleth/{attribute}/delta` endpoint similarly returns a continuous
color mapping on delta magnitude with no threshold marker. The diverging
DeltaChoropleth visualization maps the delta distribution, not the threshold
distance. CLAUDE.md's "Coffin Corner" concept requires explicit modeling of the
narrowing policy maneuver space — which requires threshold tracking, not just
continuous delta computation.

---

### Intergenerational Equity Advocate Agent — CHALLENGE

**Finding 10: Issue #69 deferred confidence tier degradation means M3
projections carry misleading confidence — immediate M4 design consequence.**

Issue #69 (ia1_disclosure compliance exception) defers time-horizon confidence
tier degradation to Milestone 4. In M3, a scenario advanced 3 steps carries
`confidence_tier` values derived from the initial attribute data quality —
typically tier 2 (IMF WEO primary source). A future Demographic module
generating 20-year population projections will produce outputs that carry the
tier of the demographic data source (likely tier 2 from UN Population Division),
not a tier reflecting 20-year projection uncertainty. When the Human Cost
Ledger surfaces a tier-2 projection of intergenerational capability loss at
year 20, the tier signals "this was sourced from UN Population Division primary
data" — not "this 20-year projection of an uncalibrated model has meaningful
uncertainty."

The M4 architecture for the Human Cost Ledger should define how
`confidence_tier` will degrade with projection horizon before implementing the
Demographic module. Implementing the module against the current tier semantics
and retrofitting degradation afterward is a breaking change to all existing
M4 snapshot outputs.

**Finding 11: Tombstone does not capture entity state at scenario creation —
reconstruction baseline is incomplete.**

`scenario_deleted_tombstones` captures `name`, `configuration JSONB`,
`scheduled_inputs JSONB`, `engine_version`, and `original_created_at`. Under
SA-11, reconstruction requires: same configuration + same scheduled inputs +
same engine version + same initial entity state. The initial entity state — the
actual attribute values in `simulation_entities` at the moment the scenario was
created — is not in the tombstone.

If the Natural Earth loader is re-run between tombstone creation and
reconstruction attempt, entity attribute values may differ. A Greece scenario
tombstoned under NE loader v1 (10 Level 1 attributes) and reconstructed after
NE loader v2 (with additional attributes) will produce different outputs even
if configuration, scheduled_inputs, and engine_version match. The SA-11
guarantee is asserted over three variables; the tombstone preserves two.

For intergenerational analysis — where scenarios may need to be reconstructed
years after original creation to verify that policy advice remained sound —
this is not a corner case. It is the primary use case.

---

### Community and Cultural Resilience Agent — CHALLENGE

**Finding 12: Module capability registry not updated for M3 — council agents
reading M2 capability state.**

`docs/scenarios/module-capability-registry.md` is dated 2026-04-21 (Milestone 2
boundary). It does not reflect M3 additions: the scenario configuration tables,
`WebScenarioRunner` execution layer, `POST /advance` time acceleration,
comparative scenario output, or the Greece backtesting fixture. A Domain
Intelligence Council member activating a scenario review after M3 and reading
the capability registry will produce findings against a capability picture that
is one milestone out of date. This affects the quality of every future council
review until the registry is updated.

More structurally: the registry documents what the simulation "can model" and
"cannot currently model." The scenario engine (M3) should appear in the "can
model" section with its capability scope, limitations, and
`WebScenarioRunner`-specific constraints (no domain modules active, DIRECTION_
ONLY backtesting thresholds, single-attribute comparison). Its absence from
the registry means council agents have no authoritative source for what M3's
scenario capabilities actually are.

**Finding 13: Level 1 resolution and community impacts — ARCH-REVIEW-002
BI2-N-09 carried forward, compounded by M3 advance capability.**

`POST /advance` enables multi-step scenario execution. Multiple steps of a
Greece scenario produce multiple GRC snapshots — one country, 3 steps, each
snapshot containing GRC-level attribute deltas. The advance capability
compounds the Level 1 resolution gap: not only can the simulation not represent
subnational differentiation within a step, it now produces a time-series of
undifferentiated national averages that users may animate or display as
trajectory graphs. A trajectory graph of Greek GDP growth and unemployment from
2010 to 2012 looks informative; it conceals that Thessaly's unemployment
trajectory, island communities' emigration pattern, and rural clinic closure
rates are all lost behind the national average at every step.

The advance capability is correct and valuable. But the temporal dimension it
adds amplifies the interpretive risk of Level 1 resolution — each additional
step of apparent analytical depth is a step deeper into an averaging operation
that destroys subnational community signal.

---

### Investment and Capital Formation Agent — CHALLENGE

**Finding 14 (RISK-AVERSE): Comparative scenarios have no step-alignment
validation — cross-step comparison silently produces misleading deltas.**

`GET /scenarios/compare?scenario_a={id_a}&scenario_b={id_b}&attribute={attr}&step={N}`
returns a `DeltaRecord` at step N. If scenario_a was advanced 5 steps and
scenario_b was advanced only 3 steps, requesting a comparison at step 4 returns
a delta where scenario_a's step-4 state is compared to scenario_b's state at
step 3 (its last available snapshot). The API should return 404 or 422 when the
requested step does not exist in one scenario's snapshot history. If the API
silently falls back to the nearest available step, the delta is computed between
temporally misaligned states with no error signal. From the ADR-004 schema, the
comparison logic fetches snapshot by `(scenario_id, step)` — if no row exists,
the behavior is determined by the JOIN type. If a LEFT JOIN is used, missing
snapshot data produces NULL deltas; if INNER JOIN, it produces empty result
rather than an error.

Investment analysis that uses comparative output to evaluate policy alternatives
cannot trust deltas computed across temporally misaligned scenarios.

**Finding 15 (RISK-TOLERANT): Fidelity report is printed text, not
machine-readable — cannot track model fidelity evolution over time.**

`fidelity_report.py` generates a structured fidelity report printed to CI logs.
This report captures whether the Greece fixture passed or failed and the
magnitude of deviations. But the output is plain text to stdout. There is no
JSON artifact, no database record, no historical store of fidelity report
outputs. When the Greece fixture is extended to 2015 (Issue #142) or when the
Thailand 1997–2000 case is added (Issue #141), the fidelity history across CI
runs will not be available for trend analysis.

Model fidelity improvement is the primary mechanism by which WorldSim becomes
credible for sovereign policy use. Tracking fidelity across time — "in June
the Greece case was passing with a 12% direction error; in August it was 8%"
— requires a persistent fidelity artifact, not a log line. The current
architecture cannot support this analysis.

**Finding 16 (CATALYTIC): Tombstone enables scenario reconstruction — but
reconstruction path has no API endpoint.**

The tombstone design correctly preserves configuration + scheduled_inputs for
deleted scenarios. Under SA-11, this enables reconstruction from first
principles. But there is no `POST /scenarios/restore` endpoint that accepts a
tombstone ID and reconstructs the scenario into the live `scenarios` table.
Reconstruction requires: (1) reading from `scenario_deleted_tombstones`, (2)
creating a new scenario with the tombstoned configuration, (3) re-advancing the
scenario step by step. This is a multi-step manual operation with no API path.

For investment analysis contexts — where a scenario was run, evaluated,
deleted, and later needs to be compared against a new scenario — the tombstone
without a restore API is an archival artifact, not an operational capability.
The design is sound; the operational path is incomplete.

---

### Social Dynamics and Behavioral Economics Agent — CHALLENGE

**Finding 17: DeltaChoropleth percentile scale obscures social contagion
signals.**

`DeltaChoropleth.tsx` computes the color scale based on the distribution of
deltas across all entities in the comparison. Percentile-based step computation
normalizes the display: the most-negative delta country is always dark crimson,
the most-positive is always dark navy, regardless of absolute delta magnitude.
If all countries in a scenario comparison experience negative GDP growth deltas
(a globally contractionary scenario), the color scale still produces the full
range from crimson to navy — the map shows apparent winners and losers when all
countries are losing.

For social contagion analysis, what matters is not relative position but
absolute threshold: when multiple countries simultaneously cross negative
thresholds for reserve coverage, unemployment, or GDP growth, the map should
show coordinated red. A percentile-normalized scale suppresses coordinated
global downturns — exactly the signal most relevant to financial contagion,
coordinated social unrest, and multi-country debt crises.

**Finding 18: ControlInput social response feedback gap — ARCH-REVIEW-002
BI2-N-10 carried forward, compounded by advance capability.**

`POST /advance` enables multi-step execution with configurable step count.
Each step fires any scheduled `ControlInput` instances for that step. The
social response to step-1 `ControlInput` effects — strikes, electoral shifts,
protest movements — has no endogenous pathway into the step-2 simulation.
The Greek austerity timeline ran as: program accepted 2010 → first general
strike May 2010 → second general strike October 2010 → parliamentary crisis
June 2011. Each step's social response affected the next step's political
capacity.

The advance capability now makes this gap more visible operationally: a 5-step
scenario executes 5 sequential rounds of scripted `ControlInput` injection
with no opportunity for social dynamics to feed back into the input sequence.
Each step is a clean injection. The simulation models a policymaker operating
in a social vacuum.

---

### Chief Methodologist Agent — CHALLENGE

**Finding 19: Snapshot envelope versioning has no migration path — M4 module
additions will produce mixed-envelope snapshots.**

`ScenarioSnapshotRepository` writes `state_data` with `_envelope_version: "1"`
as a metadata key in the JSONB. This is correct architectural hygiene — it
allows future readers to detect the schema version. But there is no migration
mechanism specified in ADR-004 for reading old-envelope snapshots alongside
new-envelope snapshots.

When M4 introduces a Demographic module that adds structured human development
fields to the snapshot state_data (for example, by adding a `human_cost_ledger`
subkey), snapshots from M4-onward runs will have `_envelope_version: "1"` (same
version) but structurally different contents. The `GET /scenarios/{id}/snapshots`
endpoint returns all snapshots for a scenario — if a scenario was partially
advanced under M3 and then advanced further under M4 with the Demographic module
active, the returned snapshots are structurally heterogeneous under the same
envelope version. A client reading step-1 through step-3 snapshots (M3,
financial only) and step-4 through step-6 snapshots (M4, with human cost data)
cannot distinguish them without reading the content, not the metadata.

The fix is simple: increment `_envelope_version` to `"2"` when M4 modules
add structural fields. But the design needs to specify when version increments
are required so that the increment happens rather than being overlooked.

**Finding 20: DIRECTION_ONLY thresholds remain the only backtesting validation
criterion — three steps does not substantively address BI2-I-03.**

M3 extends the Greece fixture from 2 steps (2010–2012) to 3 steps (2010–2013
equivalent per the 2012 endpoint data). With 2 indicators (GDP growth direction,
unemployment direction) × 3 steps = 6 sign checks, the false-positive rate
under a null model drops from 25% (2 checks) to 1.6% (6 independent checks at
50% each). This is genuine improvement.

But DIRECTION_ONLY thresholds remain a sign check. The historical magnitude of
Greek GDP contraction over this period (cumulative -25% of GDP) is not tested.
A model producing -0.01% GDP growth per step passes identically to one
producing -8% per step. In M3, "backtesting pass" still means "direction
correct on six binary tests." CLAUDE.md states "outputs are distributions, not
point estimates" — backtesting validation of a sign check does not validate
distributional accuracy, magnitude, or model fitness. The compliance posture
entry ("SCAN-012 — Greece backtesting fixture: Clean") should not be read as
validating model quantitative accuracy.

The Chief Methodologist recommends that the backtesting documentation include
an explicit statistical power statement on every fidelity report: what "PASS"
means and what it does not mean.

**Finding 21: Module capability registry is the council's authoritative
capability source — its staleness is a governance defect, not a documentation gap.**

The module capability registry dated 2026-04-21 is the document council agents
read to understand current simulation capabilities before any scenario review
or architecture challenge. It is currently one milestone out of date. M3
additions — scenario engine, advance capability, comparative output, tombstone
design — are absent. A council review conducted after M3 without updating this
registry produces findings against M2 capabilities. Some findings will target
limitations that M3 has addressed; the council's time is spent on already-solved
problems.

More importantly, the capability registry documents what conclusions are safe
to draw from simulation outputs. The M3 "Safe conclusions" section should
include: "Direction of multi-step propagation through scripted ControlInput
sequences" — an advance from M2's single-step propagation. And the "Conclusions
that should not be drawn" section should include: "Endogenous module dynamics
(no domain modules are active; all output reflects ControlInput propagation
only)." Absent this, users and council agents overestimate what M3 simulation
outputs represent.

---

## Blindspot Inventory

### Immediate Blindspots (7)
*Affect Milestone 4 design directly, create backward-incompatible risks if
not resolved before M4 module implementation begins, or mis-state the current
compliance posture.*

| ID | Finding | Agent(s) | Risk if unaddressed |
|---|---|---|---|
| BI3-I-01 | `ia1_disclosure` NOT NULL is syntactically enforced but semantically void — empty string satisfies the constraint | Development Economist, Political Economist, Intergenerational Advocate | Compliance exception documented but not surfaced to users; decade-long M4 projections will carry misleading confidence tier signals |
| BI3-I-02 | Snapshot envelope version `"1"` has no migration path — M4 module additions produce structurally heterogeneous snapshots under the same version | Chief Methodologist, Development Economist | M4 Demographic module snapshots mixed with M3 financial-only snapshots in same API response; client-side interpretation requires content-level parsing, not metadata-level routing |
| BI3-I-03 | WebScenarioRunner runs without domain modules — M3 outputs reflect ControlInput propagation only with no endogenous dynamics; no snapshot field signals this | Development Economist, Chief Methodologist | Users and council agents may interpret M3 scenario outputs as full simulation results; M3 and M4 snapshots will be structurally indistinguishable to API consumers |
| BI3-I-04 | Tombstone does not capture entity state at scenario creation — SA-11 determinism guarantee covers 2 of 3 required conditions | Intergenerational Advocate, Investment Agent | Scenario reconstruction from tombstone after entity attribute update starts from a different baseline; reproducibility guarantee is incomplete |
| BI3-I-05 | Module capability registry is dated 2026-04-21 (M2) — M3 scenario engine capabilities and limitations not documented | Community Resilience, Chief Methodologist | Council reviews conducted against M2 capability picture; safe/unsafe conclusion guidance absent for M3 scenario outputs |
| BI3-I-06 | Greece fixture initial state has no human development attributes — unemployment threshold tests direction of an unseeded attribute | Development Economist | Human cost fidelity threshold passes vacuously; unemployment direction is tested without an initial unemployment stock from which to trend |
| BI3-I-07 | Comparative output has no step-alignment validation — cross-step delta computation produces no error when one scenario has fewer snapshots than the requested step | Investment Agent | Silently misaligned scenario comparisons produce meaningless deltas in investment analysis workflows |

### Near-Term Blindspots (10)
*Affect M4 module design, compound existing gaps, or create operational
limitations in multi-scenario analysis workflows.*

| ID | Finding | Agent(s) | Risk if unaddressed |
|---|---|---|---|
| BI3-N-01 | Confidence tier degradation with projection horizon deferred (Issue #69) — M4 Human Cost Ledger will introduce long-horizon projections without degraded tier signals | Intergenerational Advocate, Development Economist | Multi-decade capability loss projections carry tier-2 confidence signals implying primary source quality rather than projection uncertainty |
| BI3-N-02 | Engine_version is a declaration, not a verifiable pointer — SA-11 determinism guarantee cannot be verified within a semver release | Geopolitical Analyst, Chief Methodologist | Within-version code changes produce result divergence under the same engine_version string; Issue #139 (M4 resolution) tracks this but the gap affects all M3 scenario comparisons |
| BI3-N-03 | DeltaChoropleth color scale is percentile-relative, not threshold-absolute — global downturns display as mixed winners/losers | Social Dynamics, Ecological Economist | Financial contagion and coordinated multi-country crises suppressed visually; social panic signals and ecological threshold crossings indistinguishable from noise |
| BI3-N-04 | Fidelity report is printed text, not machine-readable artifact — model fidelity history cannot be tracked across CI runs | Investment Agent, Chief Methodologist | Fidelity improvement over time is the primary model credibility signal for sovereign policy use; untracked fidelity cannot compound into credibility |
| BI3-N-05 | Tombstone has no restore API endpoint — tombstone reconstruction requires manual multi-step operation with no API path | Investment Agent | Deleted scenario reconstruction for cross-scenario comparison is operationally unavailable; tombstone is archival only |
| BI3-N-06 | Scenario configuration has no political legitimacy initial state — ARCH-REVIEW-002 BI2-N-02 carried forward | Political Economist, Social Dynamics | Every scenario assumes neutral political environment; M4 HCL outputs for politically constrained reforms will be systematically optimistic |
| BI3-N-07 | StateCondition cannot model compound triggers — ARCH-REVIEW-002 BI2-N-03 carried forward | Political Economist, Social Dynamics | Bank runs, capital flight, and electoral triggers require multi-attribute compound conditions; single-attribute threshold remains the only contingent mechanism |
| BI3-N-08 | Multi-step advance amplifies Level 1 resolution averaging — subnational community impacts invisible at every step | Community Resilience | Trajectory graphs of country-level indicators conceal subnational differentiation; advance capability deepens interpretive risk of averaged national data |
| BI3-N-09 | ControlInput social response feedback absent — multi-step advance executes scripted inputs in a social vacuum | Social Dynamics, Political Economist | Greek austerity backlash affected implementation capacity for subsequent inputs; 5-step scenarios model frictionless multi-year adjustment |
| BI3-N-10 | DIRECTION_ONLY thresholds remain the sole backtesting validation criterion — "backtesting pass" signals direction, not magnitude | Chief Methodologist | Six-check sign validation presented as empirical model validation; quantitative accuracy unverified; all subsequent backtesting cases will inherit this limitation unless explicit statistical power statement is added to fidelity reports |

### Long-Term Blindspots (5)
*Architectural vision issues for Milestone 4 and beyond.*

| ID | Finding | Agent(s) | Risk if unaddressed |
|---|---|---|---|
| BI3-L-01 | Ecological attributes entirely absent from entity store — ecological scenarios have no initial conditions; tombstones of financial scenarios cannot seed ecological reconstruction | Ecological Economist | Climate module implementation in a future milestone will find no ecological baseline; every ecological scenario starts from zero |
| BI3-L-02 | MDA (Minimum Descent Altitude) threshold system has no data representation — CLAUDE.md specifies hard floors with qualitatively different status below them; no threshold registry or threshold-crossing detection | Ecological Economist, Geopolitical Analyst | Hard floors (3-month reserve coverage, debt/GDP critical threshold) cannot be marked on comparative outputs; delta visualization cannot distinguish strategic discontinuities from marginal changes |
| BI3-L-03 | Coercive dynamics absent from ControlInput — IMF conditionality, sanctions, and external pressure modeled as unilateral sovereign decisions | Geopolitical Analyst | All conditionality-driven scenarios misrepresent the mechanism; coercive inputs require a new `InputSource` value and a `coercing_actor` field at minimum |
| BI3-L-04 | Snapshot architecture supports terminal-state comparison; cumulative welfare analysis requires N serial API calls — ARCH-REVIEW-002 BI2-N-08 carried forward | Intergenerational Advocate, Chief Methodologist | Human cost ledger's most important output (integral of capability loss over multi-year scenario) is not computable from a single API call; trajectory endpoint remains absent |
| BI3-L-05 | Social fabric modeled as entity attribute rather than relationship property — ARCH-REVIEW-002 BI2-L-01 carried forward; M3 advance capability deepens the gap | Community Resilience | Community solidarity networks and trust relationships remain unrepresentable at all; multi-step scenarios model national averages with no network structure |

---

## Recommended GitHub Issues

### Immediate Blindspots — Issues to Create

| Issue title | Finding ID | Labels |
|---|---|---|
| `arch(compliance): ia1_disclosure semantic validation — require non-empty structured disclosure string, not just NOT NULL` | BI3-I-01 | enhancement, horizon:immediate |
| `arch(schema): add _modules_active metadata to snapshot envelope — distinguish M3 (no modules) from M4 (domain modules) snapshots` | BI3-I-02 | enhancement, horizon:immediate |
| `docs(scenario): add modules_active field to SnapshotResponse — surface whether domain modules contributed to each snapshot` | BI3-I-03 | documentation, horizon:immediate |
| `arch(tombstone): add entity_state_snapshot to scenario_deleted_tombstones — capture simulation_entities attribute values at scenario creation time` | BI3-I-04 | enhancement, horizon:immediate |
| `docs(registry): update module capability registry to M3 — add scenario engine, advance, comparative output, and tombstone to can/cannot model sections` | BI3-I-05 | documentation, horizon:immediate |
| `arch(backtesting): seed Greece 2010 initial state with WDI human development attributes — unemployment stock, health expenditure, net enrollment` | BI3-I-06 | enhancement, horizon:immediate |
| `arch(api): add step-alignment validation to GET /scenarios/compare — return 422 if requested step exceeds either scenario's snapshot count` | BI3-I-07 | enhancement, horizon:immediate |

### Near-Term Blindspots — Issues to Create

| Issue title | Finding ID | Labels |
|---|---|---|
| `feat(schema): implement projection-horizon confidence tier degradation — address Issue #69 ia1_disclosure compliance exception for M4 long-horizon outputs` | BI3-N-01 | enhancement, horizon:near-term |
| `arch(engine): add engine_version_hash field alongside engine_version semver — git commit hash for verifiable SA-11 determinism` | BI3-N-02 | enhancement, horizon:near-term |
| `feat(frontend): add absolute threshold overlay to DeltaChoropleth — user-defined or system MDA thresholds shown as choropleth breakpoint regardless of percentile distribution` | BI3-N-03 | enhancement, horizon:near-term |
| `arch(backtesting): persist fidelity report as JSON artifact — enable cross-run fidelity tracking and model improvement trending` | BI3-N-04 | enhancement, horizon:near-term |
| `feat(api): add POST /scenarios/restore endpoint — reconstruct scenario from tombstone into live scenarios table` | BI3-N-05 | enhancement, horizon:near-term |
| `feat(scenario): add political_context to scenario configuration — initial legitimacy state, electoral calendar, coalition stability` | BI3-N-06 | enhancement, horizon:near-term |
| `feat(orchestration): implement compound StateCondition — multi-attribute AND/OR trigger logic` | BI3-N-07 | enhancement, horizon:near-term |
| `docs(scenario): add subnational resolution disclaimer to all advance endpoint outputs — Level 1 averaging documented in API response metadata` | BI3-N-08 | documentation, horizon:near-term |
| `feat(orchestration): add social response event generation — ControlInputs above legitimacy threshold generate endogenous backlash events in next timestep` | BI3-N-09 | enhancement, horizon:near-term |
| `standards(backtesting): add statistical power statement to all fidelity reports — explicit statement of what DIRECTION_ONLY PASS does and does not validate` | BI3-N-10 | documentation, horizon:near-term |
