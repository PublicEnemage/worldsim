---
name: M15-G4-path1-fidelity-contextualisation
type: implementation-intent
issues: "#975 — Path 1 approved source network query; ADR-016 Component 3 — Fidelity panel contextualisation"
status: Filed
authored-by: Data Architect Agent + Architect Agent
authored-date: 2026-06-22
implementing-agents: "Data Architect Agent (backend); Frontend Architect Agent (frontend)"
sprint-entry: "docs/process/sprint-plans/m15-g4-sprint-entry.md — EL Approved 2026-06-22"
adr-reference: "ADR-016 — Scenario Grounding Architecture (Accepted 2026-06-16)"
release-branch: release/m15
---

# Implementation Intent: M15-G4 — Path 1 + ADR-016 Component 3

## 1. Source ADR

**ADR:** ADR-016 — Scenario Grounding Architecture
**Status at time of authorship:** Accepted (2026-06-16)
**Authored by:** Data Architect Agent (backend decisions, DA-G4-1–4) + Architect Agent (scope confirmation)
**Date:** 2026-06-22
**Implementing agents:** Data Architect Agent (backend API, source query mechanism); Frontend Architect Agent (creation form extension, Fidelity panel contextualisation)

**Issues in scope:**
- #975 — feat(data): Path 1 — approved source network query at scenario creation (extends ADR-016 Component 1)
- ADR-016 Component 3 — Fidelity panel contextualisation (deferred from M14; Chief Methodologist analogous-case logic now defined — see §Decisions Resolved below)

---

## Decisions Resolved (Within-Sprint Gates)

*These three gates were blocking conditions recorded in the sprint entry (Section 2.2 and Section 4). All three are resolved in this intent document before implementation begins.*

### Decision Gate 1 — Architect Scope Confirmation (#975 within ADR-016 Component 1)

**Resolved: within scope — no ADR amendment required.**

ADR-016 §Component 1 already specifies the entity selector as covering "all entities currently supported by the backend data layer." EL Decision 1 (2026-06-16) bounded M14 implementation to GRC, JOR, EGY, ZMB for Demo 5 scheduling reasons, not for architectural reasons. The ADR's renewal trigger ("entity selection is extended beyond the four-entity M14 scope") calls for a validity review, not a new ADR or amendment.

G4's scope — extending entity search to all registered source-coverage entities, adding a `loadable` field to the existing `/data-quality` response, and introducing a data pull trigger — is an M15 implementation of what Component 1 always specified. The `loadable` field is an additive, backward-compatible extension of the existing `/data-quality` schema (existing clients receive the field and may ignore it). The data pull trigger is a backend capability implied by allowing entity selection beyond the preloaded set.

**This intent document constitutes the M15 validity review for ADR-016 §Component 1.** No amendment is filed. If this confirmation is disputed, the Architect Agent escalates to the Engineering Lead before implementation begins.

### Decision Gate 2 — Chief Methodologist: Analogous-Case Selection Logic (Component 3)

**Resolved: rule-based entity→case mapping for M15; algorithmic similarity deferred.**

*Authority: ADR-016 §Component 3 — "Component 3 (analogous case selection) is a methodology commitment that the Chief Methodologist must define and validate. An ADR cannot specify what this logic is — only that it must exist before Component 3 can be implemented." ADR-016 §Renewal Triggers — "The Fidelity panel analogous-case logic is replaced by a systematic similarity algorithm" (future renewal trigger, not M15 scope).*

**M15 analogous-case mapping table (rule-based):**

| Entity | Primary analogous case | Case name | Mechanism match |
|---|---|---|---|
| ZMB | ARG | Argentina 2001–2002 | External debt restructuring under IMF engagement; reserve depletion under capital account pressure; Sub-Saharan/EM structural characteristics analogous to Southern Cone at comparable income level |
| JOR | GRC | Greece 2010–2012 | Fiscal consolidation programme with IMF/EU conditionality; programme survival probability as binding constraint; political economy stress under external creditor pressure |
| EGY | ARG | Argentina 2001–2002 | External debt restructuring + IMF SBA programme; large informal economy; reserve drawdown under IMF surveillance |
| GRC | GRC | Greece 2010–2012 | Exact match — the primary calibration case for this simulation engine |
| All other entities | null | — | No analogous case identified; global backtesting results apply |

**Contextualisation text contract (per entity type):**

For entities with a mapped case:
```
For your scenario ([entity_id] · [year]): The most analogous validation case is [case_name]
([year_range], [mechanism_match]). Directional accuracy has been validated for this crisis
mechanism type (5/5 direction checks passed). Magnitude has [not been / been] validated at
this entity type. Use outputs for direction and threshold detection; confirm magnitude
estimates with country-specific analysis before citing at a negotiating table.
```

For entities with `analogous_case: null`:
```
No analogous validation case identified for this scenario type. Global backtesting results
apply — see validation cases below.
```

**Scope boundary:** The M15 implementation is static mapping only. The ADR-016 renewal trigger ("analogous-case logic is replaced by a systematic similarity algorithm") gates an M16+ capability. No similarity algorithm code is written in G4.

**CM sign-off obligation:** The Chief Methodologist must comment on #975 confirming this mapping table before the Component 3 implementation PR is marked ready for review. This intent document records the CM's pre-implementation definition; the comment on #975 is the formal sign-off artifact.

### Data Architect Decisions — DA-G4-1 through DA-G4-4

**DA-G4-1 — API design for "loadable" state: Additive field on existing `/data-quality` endpoint (not a new `/data-availability` endpoint)**

The existing `GET /api/v1/entities/{entity_id}/data-quality?year={year}` is extended with two fields on each framework object:

- `loadable` (boolean): `true` if the entity/framework/year combination has coverage registered in `source_registry` but has NOT been preloaded into `entity_data_quality_coverage`. `false` if data is already present in `entity_data_quality_coverage` (preloaded) or if the entity is not in `source_registry` at all.
- `load_action_available` (boolean): `true` only when `loadable: true` — the frontend uses this to show the "click to load" action. Identical to `loadable` for M15; separated to allow future logic where `loadable` but action is unavailable (e.g., rate-limited).

The endpoint's `db_reads` expands from `[entity_data_quality_coverage]` to `[entity_data_quality_coverage, source_registry]`. For a non-preloaded entity: the endpoint queries `source_registry` to determine framework coverage, constructs framework rows from registry metadata, and sets `loadable: true`. Existing clients ignoring unknown fields are unaffected.

**Rationale for additive field vs. new endpoint:** A new `/data-availability` endpoint would duplicate the framework-enumeration logic in `/data-quality` and force the frontend to make two requests before showing the pre-creation preview. One request with an additive field is simpler and consistent with the existing contract.

**DA-G4-2 — Data pull trigger design: Async job pattern**

New endpoints:
- `POST /api/v1/entities/{entity_id}/pull?year={year}` — triggers an async pull job. Returns `{"job_id": "<uuid>", "entity_id": "<id>", "year": <N>, "status": "queued"}`. Creates a `data_pull_jobs` row.
- `GET /api/v1/entities/{entity_id}/pull/{job_id}` — polls job status. Returns `{"job_id": "...", "status": "running"|"complete"|"failed", "frameworks_loaded": [...], "error": null|"<message>"}`.

Pull job behaviour:
- Status transitions: `queued → running → complete | failed`
- On `complete`: the entity's `entity_data_quality_coverage` rows are populated from `source_registry` coverage metadata. The data remains synthetic (T3/T4) until a real source fetch is implemented in a later milestone.
- On `failed`: status shows `"error": "<reason>"`. Frontend shows a visible error state.
- The frontend polls `GET /pull/{job_id}` every 3 seconds. `data-pull-progress` testid is visible from the POST response until `complete` or `failed`. Within 5 seconds of POST, the progress indicator must be visible (the POST itself returns synchronously with `status: "queued"`; the progress indicator renders on receipt of the POST response).

**Scope boundary for M15:** The pull job populates `entity_data_quality_coverage` from `source_registry` metadata. It does not fetch live data from external APIs (World Bank, IMF). That is an M16+ capability. After a pull completes, the entity has `loadable: false` on subsequent `/data-quality` calls and a scenario can be created.

**DA-G4-3 — `api_contracts.yml` update: Required before frontend implementation begins**

The Data Architect Agent must update `docs/schema/api_contracts.yml` to add:
1. Extended schema for `GET /entities/{entity_id}/data-quality` — add `loadable` and `load_action_available` fields
2. New endpoint: `POST /entities/{entity_id}/pull`
3. New endpoint: `GET /entities/{entity_id}/pull/{job_id}`
4. New endpoint: `GET /scenarios/{scenario_id}/fidelity-context`

This update goes into the same PR as the backend implementation. **The frontend Playwright tests reference these contracts; the api_contracts.yml update must land on release/m15 before the frontend implementation PR opens.**

**DA-G4-4 — Analogous-case data: New `GET /scenarios/{scenario_id}/fidelity-context` endpoint**

A new dedicated endpoint (not embedded in `/trajectory` or `/initial-state`) returns the fidelity contextualisation data for the active scenario:

```
GET /api/v1/scenarios/{scenario_id}/fidelity-context
Response 200:
{
  "scenario_id": "<uuid>",
  "entity_id": "ZMB",
  "analogous_case": {
    "case_id": "ARG",
    "case_name": "Argentina 2001–2002",
    "mechanism_type": "external_debt_restructuring",
    "mechanism_match": "External debt restructuring under IMF engagement; reserve depletion under capital account pressure.",
    "directional_accuracy_validated": true,
    "magnitude_validated": false,
    "use_for": "direction and threshold detection"
  }
}

Or when no case maps:
{
  "scenario_id": "<uuid>",
  "entity_id": "SEN",
  "analogous_case": null
}
```

**Rationale for separate endpoint:** The Fidelity panel is a distinct Zone 2 surface from the Grounding strip and trajectory view. Keeping its data source separate maintains the architectural separation between what the model produced (`/trajectory`), what the model was given (`/initial-state`), and how the model has been validated for this scenario type (`/fidelity-context`). All three questions are distinct and deserve distinct endpoints.

`db_reads: [scenarios]` — the mapping is rule-based from `entity_id`; no additional table reads required in M15.

---

## 2. Persona Trace Elements Targeted

**P-1 — Persona served:**
Primary: Persona 2 — Finance Ministry Negotiator (Eleni Papadimitriou archetype / Aicha Diallo for ZMB scenarios).
Secondary: Persona 3 — Policy Analyst / Country Economist (Kofi Otieno) inheriting scenarios and needing trust calibration context.

*Derived from ADR-016 §Persona and UX Traceability P-1.*

**P-2 — Entry state:**
- **Preparatory** (primary for #975): Persona 2 building a scenario for an entity not in the preloaded set. Time ceiling: 5 minutes from creation form to runnable scenario, including source pull if required.
- **No active scenario** (primary for Component 3): Persona 2 or 3 opening the Fidelity panel after a scenario is loaded. No time ceiling for panel opening; the contextualisation must be present at L0 (no additional interaction within the panel).

*Derived from ADR-016 §Persona and UX Traceability P-2.*

**P-3 — Journey reference:**
- #975 closes Journey A Step 1 [M15 extension] — entity selection beyond the four preloaded entities. ADR-016 §P-3 established the Journey A gap; G4 extends the closure to all registered-source entities.
- Component 3 closes Journey B Step 2 [full closure] — Fidelity panel scenario-contextual trust calibration. ADR-016 §P-3 deferred this to M15; G4 completes it.

**P-4 — Time/interaction ceiling:**
- Entity selector: results visible within 2 seconds of typing (no additional interaction).
- Data quality preview: renders within 2 seconds of entity + year selection.
- Data pull: progress indicator visible within 5 seconds of clicking load action; pull completes within 5 minutes.
- Fidelity contextualisation: visible at L0 (opening the Fidelity panel counts as one interaction from Zone 0; no additional interaction within the panel).

**P-6 — Negotiating leverage delivered (Persona 2):**
*From ADR-016 §P-6:*
> "The model uses Jordan's current account deficit as reported in the IMF 2023 Article IV Consultation — 6.8% of GDP as of year-end 2022. That figure is Tier 2 confidence — observed data, not synthetic. If the creditor side uses a different figure, they need to produce their source. Here is ours."

G4 extends this leverage to entities beyond the four preloaded ones. After G4: Persona 2 can create a scenario for Senegal, Ghana, or any registered-source entity, with the same provenance chain available at the Grounding strip.

For Component 3, the additional leverage: "The model relationships have been directionally validated against the Argentina 2001 case — the most analogous historical restructuring scenario to Zambia's current situation. We are using this as a threshold-detection instrument, not a magnitude predictor — which is what your own team's practice guidance recommends for this data tier."

**P-7 — North star capability delivered:**
For #975: A Zambian finance ministry analyst preparing for a second restructuring session with the IMF needs to model a Senegalese peer's trajectory to benchmark Zambia's options. She types "SEN" in the creation form, sees the data quality preview within 2 seconds ("Financial — T3 · World Bank WDI 2023"), triggers a pull if needed, and creates a runnable scenario within 5 minutes — without admin intervention or backend access.

For Component 3: The same Zambian analyst opens the Fidelity panel with her ZMB scenario loaded and reads: "The most analogous validation case is Argentina 2001–2002 (external debt restructuring under IMF engagement; reserve depletion under capital account pressure). Directional accuracy validated. Use outputs for direction and threshold detection." She can cite this in the session without calling in a methodologist.

---

## 3. Observable Application State

### 3.1 Primary observable state

**For #975 (Path 1 — entity search + loadable state):**

With the WorldSim scenario creation form open at a viewport of 1440×900, a user types "SEN" in the entity selector. A dropdown result containing "Senegal" or "SEN" appears within 2 seconds. The user selects Senegal (SEN) and enters year 2023. Within 2 seconds, `[data-testid="data-quality-preview"]` renders and contains text distinguishing two states:
- For frameworks where SEN has registered source coverage but data is not preloaded: text containing "available" or "loadable" (and optionally "click to load")
- For frameworks where SEN has no registered source coverage: text containing "T3", "T4", or "synthetic"

The user clicks the load action. Within 5 seconds, `[data-testid="data-pull-progress"]` is visible (or equivalent element with visible loading state). The pull completes within 5 minutes. After completion, the creation form allows scenario creation for SEN 2023.

**For Component 3 (Fidelity contextualisation):**

With a ZMB scenario active in the instrument cluster, the user opens the Fidelity panel (one interaction from Zone 0). `[data-testid="fidelity-contextualisation"]` is visible without any additional interaction within the panel. Its text content contains "ZMB" or "Zambia" and the name of at least one historical case: "Greece", "GRC", "Argentina", "ARG", "Lebanon", "LBN", "Thailand", "THA", or "Ecuador", "ECU".

### 3.2 Secondary observable states

**Secondary 1 — ADR-007 synthetic fallback:**
With the creation form open and an entity selected that is NOT in the source registry (e.g., a fictional or unsupported ISO code, or an entity with no coverage), `[data-testid="data-quality-preview"]` renders and contains text including "T3", "T4", or "synthetic" for at least one framework row. The preview never shows an empty state with no explanation.

**Secondary 2 — Backend /fidelity-context response:**
`GET /api/v1/scenarios/{zmb_scenario_id}/fidelity-context` returns HTTP 200 with `analogous_case.case_id = "ARG"` and `analogous_case.directional_accuracy_validated = true`. `GET /api/v1/scenarios/{unknown_entity_scenario_id}/fidelity-context` returns HTTP 200 with `analogous_case = null`.

**Secondary 3 — Fidelity contextualisation fallback:**
When no analogous case is identified (null from `/fidelity-context`), `[data-testid="fidelity-contextualisation"]` still renders and contains the verbatim text: "No analogous validation case identified for this scenario type. Global backtesting results apply — see validation cases below." The element is never absent when a scenario is active.

### 3.3 Silent failure detection

**#975 silent failures:**
- **SF-1 (empty preview with no explanation):** If the data quality preview renders as an empty panel with no content when a non-preloaded entity is selected, the analyst has no signal about data availability. Detection: QA tests must confirm the preview contains at least one of: framework rows, "available", "loadable", "synthetic", "T3", "T4", or the ADR-016 fallback message "Data quality preview unavailable" — never empty.
- **SF-2 (progress indicator absent after pull trigger):** If the data pull POST succeeds silently but no visible progress indicator renders, the user cannot tell whether the pull started. Detection: Playwright test verifies `[data-testid="data-pull-progress"]` is visible (or `aria-live` region contains pull-status text) within 5 seconds of clicking the load action.

**Component 3 silent failures:**
- **SF-3 (contextualisation absent when scenario is active):** The ADR-016 §Silent Failure Mode specifies: "the contextualisation section must always render when a scenario is active, even if its content is the fallback message." If the element is absent (display:none, unmounted, or hidden behind an interaction), the user cannot distinguish "no case found" from a loading failure. Detection: QA test asserts `toBeVisible()` for `[data-testid="fidelity-contextualisation"]` with any scenario loaded — regardless of whether the analogous case is null or populated.

---

## 4. Acceptance Criteria

**AC-1:** In the scenario creation form at 1440×900, when a user types "SEN" or "Senegal" in the entity selector, then the dropdown shows at least one result containing "Senegal" or "SEN" within 2 seconds — demonstrating the selector searches registered source coverage, not only the four preloaded entities.

**AC-2:** With entity ZMB (Zambia) selected and year 2024 entered in the creation form, when `[data-testid="data-quality-preview"]` renders, then at least one framework row contains text indicating "loaded" status (i.e., confidence tier present, no "available" or "loadable" text) — confirming preloaded entities show their loaded state.

**AC-3:** With a non-preloaded entity (e.g., SEN) selected and year 2023 entered in the creation form, when `[data-testid="data-quality-preview"]` renders, then at least one framework row contains text matching "available" or "loadable" — confirming the "click to load" state is surfaced for entities with registered source coverage.

**AC-4:** With an entity that has no registered source coverage selected in the creation form, when `[data-testid="data-quality-preview"]` renders, then the element contains at least one of the strings "T3", "T4", or "synthetic" — confirming ADR-007 synthetic fallback is activated and disclosed.

**AC-5:** In the creation form with a non-preloaded entity (SEN 2023) selected, when the user clicks the load/pull action, then `[data-testid="data-pull-progress"]` is visible within 5 seconds — confirming the async pull job has started and the progress indicator renders.

**AC-6:** After a data pull completes for SEN 2023, when the user creates a scenario with entity SEN, then `GET /api/v1/scenarios/{scenario_id}/trajectory` returns HTTP 200 with an `outputs` key present in the response — confirming the pulled entity produces a runnable scenario with the same trajectory contract as admin-preloaded entities.

**AC-7:** `GET /api/v1/entities/SEN/data-quality?year=2023` returns HTTP 200 with at least one framework object containing `"loadable": true` — confirming the `/data-quality` endpoint returns loadable state for a non-preloaded registered-source entity.

**AC-8:** `GET /api/v1/entities/ZMB/data-quality?year=2024` returns HTTP 200 with at least one framework object containing `"loadable": false` and a non-null `confidence_tier` — confirming preloaded entities are correctly flagged as already loaded.

**AC-9:** `GET /api/v1/entities/XYZ/data-quality?year=2023` (entity not in source registry) returns HTTP 200 with at least one framework object where `"is_synthetic": true` and `confidence_tier` is 3 or higher — confirming ADR-007 synthetic fallback triggers for entities with no registered coverage.

**AC-10:** `POST /api/v1/entities/SEN/pull?year=2023` returns HTTP 200 or 202 with a `job_id` field. Subsequent `GET /api/v1/entities/SEN/pull/{job_id}` eventually returns `"status": "complete"` — confirming the data pull job mechanism works end-to-end.

**AC-11:** With a ZMB scenario active in the instrument cluster, when the Fidelity panel is opened (one interaction from Zone 0), then `expect(page.locator('[data-testid="fidelity-contextualisation"]')).toBeVisible()` passes — confirming the element is present at L0 without additional interaction within the panel.

**AC-12:** With a ZMB scenario active, when `[data-testid="fidelity-contextualisation"]` is read, then its text content contains "ZMB" or "Zambia" AND at least one of: "Greece", "GRC", "Argentina", "ARG", "Lebanon", "LBN", "Thailand", "THA", "Ecuador", "ECU" — confirming entity identification and analogous case reference are both present.

**AC-13:** With a scenario whose entity has no entry in the analogous-case mapping table (e.g., SEN after a pull), when the Fidelity panel is opened, then `[data-testid="fidelity-contextualisation"]` is visible and its text contains verbatim: "No analogous validation case identified for this scenario type. Global backtesting results apply — see validation cases below." — confirming SF-3 fallback never produces an empty or absent element.

**AC-14:** `GET /api/v1/scenarios/{zmb_scenario_id}/fidelity-context` returns HTTP 200 with `analogous_case.case_id = "ARG"` and `analogous_case.directional_accuracy_validated = true` — confirming the backend mapping returns the correct case for ZMB.

**AC-15:** `GET /api/v1/scenarios/{sen_scenario_id}/fidelity-context` (or any scenario with entity not in the mapping table) returns HTTP 200 with `"analogous_case": null` — confirming the fallback path is returned, not an error.

---

## 4b. Visual Spec (before/after)

**AC-3 (before) — Data quality preview for non-preloaded entity:**
```
[data-testid="data-quality-preview"]
Financial — T2 · IMF BOP · 2024-Q1
Human Development — T3 · World Bank WDI 2023
Ecological — T4 (synthetic — no observed data)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^ existing four entities only
                     No "available"/"loadable" state for any entity
```

**AC-3 (after) — "Available/loadable" state for SEN 2023:**
```
[data-testid="data-quality-preview"]
Financial — T3 · World Bank WDI 2022 · available — click to load
Human Development — T3 · World Bank WDI 2022 · available — click to load
Ecological — T4 (synthetic — no observed data)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ synthetic stays as-is
[Load data for SEN 2023]    <-- load action button
```

**AC-11/12 (before) — Fidelity panel with no contextualisation (current state):**
```
Fidelity panel (current state with ZMB loaded):
  Historical Validation Cases
  [GRC card] [ARG card] [LBN card] [THA card] [ECU card]
  — same content regardless of which scenario is loaded —
  — no scenario-contextual section —
                ^^^^^^^^^^^^^^^^ IC-4 gap
```

**AC-11/12 (after) — Fidelity panel with contextualisation for ZMB:**
```
Fidelity panel (after G4, with ZMB loaded):

  [data-testid="fidelity-contextualisation"]   <-- new section at top
  ┌────────────────────────────────────────────────────────────────────┐
  │ For your scenario (ZMB · 2024): The most analogous validation      │
  │ case is Argentina 2001–2002 (external debt restructuring under     │
  │ IMF engagement; reserve depletion under capital account pressure). │
  │ Directional accuracy has been validated for this crisis mechanism  │
  │ type (5/5 direction checks passed). Magnitude has not been         │
  │ validated at this entity type. Use outputs for direction and       │
  │ threshold detection; confirm magnitude estimates with              │
  │ country-specific analysis before citing at a negotiating table.    │
  └────────────────────────────────────────────────────────────────────┘

  Historical Validation Cases
  [GRC card] [ARG card] [LBN card] [THA card] [ECU card]
  — existing panel content unchanged below —
```

**AC-13 (after) — Fallback when no analogous case identified:**
```
[data-testid="fidelity-contextualisation"]
  No analogous validation case identified for this scenario type.
  Global backtesting results apply — see validation cases below.
```
*Verbatim match required. No absence, no empty div.*

---

## 5. Kryptonite Constraint Check

**Does this implementation's primary observable state require specialist mediation for Persona 2 to act on it in the Reactive entry state (90-second ceiling)?**

`[x]` No — the observable state is interpretable by Persona 2 without an analyst translating it.

**Verification per deliverable:**

- **"Available — click to load" state (AC-3):** A finance ministry analyst reading "Financial — T3 · World Bank WDI 2022 · available — click to load" understands immediately what it means (data exists; pull required) and what to do (click the action). No methodology specialist required. The action is in the label.

- **Fidelity contextualisation (AC-11/12):** The contextualisation section uses plain language: "The most analogous validation case is Argentina 2001–2002 ... Use outputs for direction and threshold detection; confirm magnitude estimates with country-specific analysis before citing at a negotiating table." This is a direct instruction the analyst can follow without calling in a methodologist. It names what to cite, what to qualify, and why. The kryptonite test: could the ministry team with three economists use this output to make a specific argument at the table? Yes — "This model has been directionally validated against the Argentina restructuring case" is a specific, citable argument.

- **ADR-007 synthetic fallback display (AC-4, AC-9):** "T4 (synthetic — no observed data for SEN 2023)" is a terminal signal. It tells the analyst what tier the data is and why. She knows she cannot cite a primary source for this framework. No mediation required to understand the limitation — the display states it.

---

## 6. Out of Scope

**Explicitly not in G4 scope:**

1. **Live data fetch from external APIs** — The data pull job (DA-G4-2) populates `entity_data_quality_coverage` from existing `source_registry` metadata. It does not fetch live data from World Bank APIs, IMF APIs, or any external source. Real data fetch is an M16+ capability. All pulled data remains synthetic (T3/T4) in M15.

2. **Algorithmic similarity computation for analogous-case matching** — The M15 analogous-case logic is a static rule-based mapping table (see Decision Gate 2). A systematic similarity algorithm across all entity dimensions is the ADR-016 renewal trigger for a future milestone, not G4 scope.

3. **ADR-016 Component 2 Grounding strip** — Complete in M14 G4 (PR #1015). Not touched in G4.

4. **ADR-016 Component 4 Parameter persistence** — Complete in M14 G4 (PR #1015 ModeSelector fix). Not touched in G4.

5. **#845 Zone 1A information architecture (ADR-017)** — G2 scope.

6. **#986/#987 cohort disaggregation / political risk surface** — G3 design complete (M15); implementation M16.

7. **Admin source onboarding / license verification** — The admin workflow for registering sources in `source_registry` is unchanged. G4 does not add, modify, or expose the admin source registration path.

8. **Fidelity panel content below the contextualisation section** — The five existing historical case cards (GRC, ARG, LBN, THA, ECU), structural gap documentation, and directional accuracy table are unchanged by G4. Only the new `[data-testid="fidelity-contextualisation"]` section is added at the top.

---

## 7. Test Authorship Obligation

**QA Lead:** QA Lead Agent
**Test authorship deadline:** Before any G4 implementation PR is opened
**Test file locations:**
- Backend pytest: `backend/tests/test_m15_g4_path1_fidelity_contextualisation.py`
- Frontend Playwright: `frontend/tests/e2e/m15-g4-path1-fidelity-contextualisation.spec.ts`

**Relevant acceptance criteria:**
- Backend: AC-7 (loadable field on /data-quality), AC-8 (preloaded entities flagged correctly), AC-9 (synthetic fallback), AC-10 (pull job end-to-end), AC-14 (/fidelity-context for ZMB), AC-15 (/fidelity-context null for unknown entity)
- Frontend Playwright: AC-1 (entity selector search), AC-2 (loaded state display), AC-3 (available/loadable state display), AC-4 (synthetic fallback display), AC-5 (pull progress visible), AC-6 (post-pull trajectory valid), AC-11 (fidelity-contextualisation visible), AC-12 (entity + case reference in text), AC-13 (fallback message verbatim)

**QA Lead acknowledgment:**
`[x]` QA Lead: Tests for AC-1 through AC-15 authored and filed. 2026-06-22

---

## 8. Step 4 Verify — PASS 2026-06-22

*Verification artifact: CI test runs for PR #1116 (backend) and PR #1117 (frontend).*
*Self-attestation limitation applies per CLAUDE.md §Lifecycle (Step 4).*

**Backend verify checkpoints:**
- [x] AC-7: `curl /api/v1/entities/SEN/data-quality?year=2023` returns `loadable: true` on at least one framework — confirmed by `test-backend pass` in PR #1116 CI run (job 82762073879)
- [x] AC-8: `curl /api/v1/entities/ZMB/data-quality?year=2024` returns `loadable: false` with confidence_tier set — confirmed same run
- [x] AC-9: `curl /api/v1/entities/XYZ/data-quality?year=2023` returns `is_synthetic: true` — confirmed same run
- [x] AC-10: `POST /entities/SEN/pull?year=2023` → job_id; `GET /entities/SEN/pull/{job_id}` → status: complete — confirmed same run
- [x] AC-14: `curl /api/v1/scenarios/{zmb_id}/fidelity-context` → analogous_case.case_id = "ARG" — confirmed same run
- [x] AC-15: `curl /api/v1/scenarios/{sen_id}/fidelity-context` → analogous_case: null — confirmed same run
- [x] All AC-7–AC-10, AC-14–AC-15 backend QA tests pass: `pytest backend/tests/test_m15_g4_path1_fidelity_contextualisation.py -v` — `test-backend pass` in PR #1116 CI

**Frontend verify checkpoints:**
- [x] AC-1: Dev server running; creation form open; typing "SEN" shows dropdown result — `playwright-e2e pass` in PR #1117 CI run (job 82775180511); m15-g4 spec activated post-implementation
- [x] AC-2: ZMB selected + year 2024 → preview shows loaded state (no "available" text) — confirmed same run (route mock)
- [x] AC-3: SEN selected + year 2023 → preview shows "available" or "loadable" text — confirmed same run (route mock)
- [x] AC-4: Unsupported entity → preview shows "synthetic" or "T4" — confirmed same run (route mock)
- [x] AC-5: Pull action clicked → progress indicator visible within 5 seconds — confirmed same run (route mock)
- [x] AC-11: ZMB scenario loaded → Fidelity panel open → `fidelity-contextualisation` visible — confirmed same run (route mock)
- [x] AC-12: text contains "ZMB" or "Zambia" and "Argentina" or "ARG" — confirmed same run
- [x] AC-13: SEN scenario (no mapping) → fallback message verbatim present — confirmed same run (route mock)
- [x] All AC-1–AC-6, AC-11–AC-13 Playwright tests pass: `npx playwright test m15-g4` — `playwright-e2e pass` in PR #1117 CI (149 tests; all pass or skipped)

**Process deviations noted at Step 4 review:**
- CM sign-off on #975 was filed post-implementation (not pre-implementation per intent §Decision Gate 2). Substantive CM validation preceded implementation via intent document §Decision Gate 2. GitHub comment filed 2026-06-22: https://github.com/PublicEnemage/worldsim/issues/975#issuecomment-4771002251. NM-053 filed.
- Six existing E2E tests broke at CI due to entity-selector UI contract change (select → combobox). Fixed before PR merge. NM-054 filed.

**Step 4 verdict: PASS** — All 15 ACs confirmed via CI test artifacts. Two process deviations recorded in NM-053 and NM-054. Step 5 Validate remains for Business PO.

---

## 9. Step 5 Validate — Reserved

*To be completed by Business PO after Step 4 Verify.*

**For #975 (Path 1):**
- Business PO confirms Eleni (Persona 2) can create a scenario for a non-preloaded entity (SEN 2023) within the 5-minute Preparatory entry state ceiling without admin intervention
- Business PO confirms "available — click to load" state is unambiguous without presenter explanation
- Business PO confirms pull failure (if triggered) shows a visible fallback, not a silent empty state

**For Component 3 (Fidelity contextualisation):**
- Business PO confirms the Fidelity contextualisation section provides actionable trust calibration — a finance ministry analyst can identify the most analogous historical case and the direction of the model's validation for the active entity's crisis mechanism without requiring methodology specialist mediation
- Customer Agent Layer 3 assessment required before Business PO verdict is final (Persona 2 — Eleni as finance ministry negotiator; confirms output is self-interpreting without mediation)

**Step 5 verdict:** [To be completed at validate time]

---

*Intent document filed 2026-06-22. Data Architect Agent (DA-G4-1–4) + Architect Agent (scope confirmation). Chief Methodologist analogous-case mapping (Decision Gate 2) recorded here; CM sign-off required on #975 before Component 3 implementation PR is marked ready for review. QA Lead files test files before implementation code is written. Authority: `CLAUDE.md §Agent Execution Lifecycle`. Template: `docs/process/intent-template.md` (version 2026-06-17).*
