---
name: m14-g3-sprint-entry
type: sprint-entry
milestone: M14 — Methodology Publication and External Validation
sprint-group: G3
status: EL Approved — 2026-06-17
authored-by: PM Agent
authored-date: 2026-06-17
el-approved: 2026-06-17
release-branch: release/m14
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M14, G3: ADR-016 Backend (Source Registry + Data-Quality + Initial-State)

**Status:** EL Approved — 2026-06-17
**Date authored:** 2026-06-17
**Release branch:** `release/m14`
**Sprint plan:** `docs/process/sprint-plans/m14-sprint-plan.md` (EL Approved 2026-06-16)

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).
This entry gates G3 specifically. G3 is the ADR-016 backend group — source registry population
and two new API endpoints. G3 gates G4 (ADR-016 frontend); G4 implementation PR may not open
until G3 endpoints exist and at least AC-1 and AC-6 pass in the running application.*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M14 — Methodology Publication and External Validation |
| GitHub Milestone | #15 |
| Sprint group | G3 — ADR-016 Backend |
| Release branch | `release/m14` |
| Sprint plan document | `docs/process/sprint-plans/m14-sprint-plan.md` |
| Exit checklist issue | #968 |
| Sprint groups in scope | G3 only |
| ADR gate | ADR-016 — Scenario Grounding Architecture ✅ Accepted 2026-06-16 (PR #967) |
| Implementing agents | Chief Engineer Agent (Python endpoints + source registry population); Data Architect Agent (`api_contracts.yml` update — DA holds R per `docs/process/agent-raci.md §File Ownership`) |

---

## Section 2 — Entry Invariants Checklist

*All items must be checked before any implementation PR is opened for G3.
An unchecked invariant blocks implementation from beginning.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m14` cut from `main` 2026-06-16 (PR #991 merged)
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes
  `release/m*` — confirmed 2026-06-16 (Ruleset ID 17751852 with 6 required checks: `changes`,
  `lint`, `test-backend`, `playwright-e2e`, `compliance-scan`, `branch-naming`)
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m14-sprint-plan.md`
  `el-approved: 2026-06-16` (PR #992)

### 2.2 — ADR prerequisite gate

G3 implements ADR-016 §Component 1 (`/data-quality` endpoint) and §Component 2
(`/initial-state` endpoint) at the backend layer. ADR-016 is Accepted.

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| G3 | ADR-016 — Scenario Grounding Architecture | **Accepted 2026-06-16 (PR #967)** | **CLEAR** |

- [x] ADR-016 is Accepted. G3 ADR gate is clear.

**Data Architect RACI obligation:** Data Architect Agent holds R on `docs/schema/api_contracts.yml`
per `docs/process/agent-raci.md §File Ownership`. The DA must update `api_contracts.yml` in the
same PR as the endpoint implementation — this is AC-9 of the intent document. The Chief Engineer
Agent may not mark the G3 PR ready for review without the DA's `api_contracts.yml` update included.

### 2.3 — Intent document gate

*An intent document must be filed before any G3 implementation PR opens.
(Authority: CLAUDE.md §Agent Execution Lifecycle Step 1)*

- [x] Intent document filed for G3 deliverables — **FILED 2026-06-17**

| Deliverable | ADR reference | Intent document path | Filed? |
|---|---|---|---|
| `GET /api/v1/entities/{entity_id}/data-quality` endpoint | ADR-016 §Component 1 | `docs/process/intents/M14-G3-2026-06-17-adr016-backend.md` | ✅ Filed 2026-06-17 (pending commit — same PR as this entry) |
| `GET /api/v1/scenarios/{scenario_id}/initial-state` endpoint | ADR-016 §Component 2 | (same intent document) | ✅ Filed 2026-06-17 (pending commit — same PR as this entry) |
| Source registry seed: GRC/JOR/EGY/ZMB | ADR-016 §Decision 1 | (same intent document) | ✅ Filed 2026-06-17 (pending commit — same PR as this entry) |
| `api_contracts.yml` update | ADR-016 §Decision 3 / DA RACI | (same intent document — AC-9) | ✅ Filed 2026-06-17 (pending commit — same PR as this entry) |

**Completeness gate:** The QA Lead can write pytest tests for AC-1 through AC-9 from the intent
document without reading any implementation code. The intent document specifies exact HTTP
methods, paths, query parameters, expected response shapes, HTTP status codes, fixture creation
sequences, and conftest setup obligations. Gate: PASS.

### 2.4 — QA test authorship gate

*QA tests must be authored from the intent document's acceptance criteria before implementation
code is written. (Authority: CLAUDE.md §Agent Execution Lifecycle Step 2)*

- [x] QA test file authored for G3 before implementation begins — **FILED 2026-06-17**

| Deliverable | Intent document | Test file path | Authored before implementation? |
|---|---|---|---|
| `/data-quality` endpoint (AC-1–AC-5) | `docs/process/intents/M14-G3-2026-06-17-adr016-backend.md` | `backend/tests/test_m14_g3_adr016_backend.py` (pytest + httpx) | No — author after intent document, before implementation PR |
| `/initial-state` endpoint (AC-6–AC-8) | (same intent document) | (same test file) | No — author after intent document, before implementation PR |
| Source registry coverage, all four entities (AC-4 loop) | (same intent document) | (same test file) | No — author after intent document, before implementation PR |
| `api_contracts.yml` entries (AC-9) | (same intent document) | (same test file — file-existence assert) | No — author after intent document, before implementation PR |

**Test authorship sequence:** QA Lead Agent authors `backend/tests/test_m14_g3_adr016_backend.py`
from AC-1 through AC-9 per intent document §7. Key fixture requirements:
- AC-1 through AC-5: source registry entries for GRC/JOR/EGY/ZMB must exist in the test
  database. Preferred approach (a): rely on G3's migration/seed — the seed is the deliverable and
  the test confirms it ran correctly. Approach (b): direct conftest.py insertion as fallback.
- AC-6 and AC-7: a completed JOR scenario is required. Use `POST /scenarios` + `POST
  /scenarios/{id}/run` in a `beforeAll`/fixture setup before calling `/initial-state`.
- AC-8: a pre-G3 scenario with no source-registry association. A scenario using entity_id
  `"TST"` (not in the registry) confirms 200 with empty frameworks, not 404.
- AC-9: file-existence assert that `docs/schema/api_contracts.yml` contains both new path strings.

---

## Section 3 — Scope Declaration

### 3.1 — Deliverables in scope

G3 is an ADR-implementation group with no GitHub issue numbers directly assigned — it is backend
infrastructure that unblocks G4. The sprint plan entry is: "Source registry population
(GRC/JOR/EGY/ZMB), `/data-quality` endpoint, `/initial-state` endpoint. Data Architect updates
`api_contracts.yml`. Chief Engineer implements."

| Deliverable | ADR section | Priority | Observable application state |
|---|---|---|---|
| `GET /api/v1/entities/{entity_id}/data-quality?year={year}` | ADR-016 §Component 1 | immediate | HTTP 200 for GRC/JOR/EGY/ZMB with at least one framework entry; HTTP 200 with `"frameworks": []` for unsupported entities (not 404 or 500) — AC-4, AC-5 |
| `GET /api/v1/scenarios/{scenario_id}/initial-state` | ADR-016 §Component 2 | immediate | HTTP 200 with at least one framework key and one indicator for a completed JOR scenario; HTTP 200 with `"frameworks": {}` for pre-G3 scenarios (not 404) — AC-6, AC-7, AC-8 |
| Source registry seed: GRC/JOR/EGY/ZMB | ADR-016 §Decision 1 | immediate | `/data-quality?year=2024` returns `confidence_tier ≤ 3` for Financial and HumanDevelopment frameworks per entity; ZMB returns `is_synthetic: true` with non-null `synthetic_basis` — AC-1, AC-2, AC-3 |
| `docs/schema/api_contracts.yml` update | ADR-016 §Decision 3 / DA RACI | immediate | File contains endpoint entries for both new paths with full schema matching ADR-016 §Component 1 and §Component 2 API contract specifications — AC-9 |

**G3's north star obligation (P-7):** After G3, `GET /api/v1/scenarios/{jor_id}/initial-state`
returns an indicator entry where `name == "reserve_coverage_months"`, with non-null `source`
(e.g., `"IMF BOP"`) and non-null `vintage` (e.g., `"2024-Q1"`). This specific indicator enables
the Persona 2 north star argument at G4's Grounding strip: "The model uses Jordan's current
account deficit as reported in the IMF 2023 Article IV Consultation. That figure is Tier 2
confidence. Here is our source." G4 displays it; G3 makes it queryable.

### 3.2 — Deliverables explicitly out of scope

| Scope item | Rationale for exclusion |
|---|---|
| ADR-016 Component 3 (Fidelity panel contextualisation) | Deferred to M15 by EL decision (ADR-016 §Decision 2); no backend endpoint required from G3 |
| ADR-016 Component 4 (parameter persistence) | G4 frontend scope — reads from existing `scenarios.configuration`; no new G3 endpoint |
| Entity scope beyond GRC/JOR/EGY/ZMB | EL decision (ADR-016 §Decision 1); endpoint returns 200 with empty frameworks for unlisted entities but no source registry seeding required |
| Real-time external API calls | G3 reads from `source_registry` table only — no live IMF/World Bank calls at request time |
| Per-cohort initial state disaggregation | M15+ per ADR-016 §Known Limitations |
| CI_lower / CI_upper confidence interval bands | ADR-007 pending; G3 returns `confidence_tier` (integer 1–5) only |
| G4 (ADR-016 frontend) | Gated on G3; separate sprint group with its own entry document |
| G5 (ADR-015 implementation) | Separate sprint group; no backend dependency on G3 |

---

## Section 4 — ADR Prerequisite Summary

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| G3 | ADR-016 — Scenario Grounding Architecture | **Accepted 2026-06-16 (PR #967)** | **Yes — EL approved 2026-06-17; QA tests filed PR #1011** |

**Implementation sequencing for G3:**

1. EL approves this entry document (this step)
2. QA Lead Agent authors `backend/tests/test_m14_g3_adr016_backend.py` from AC-1 through AC-9
   in the intent document — **must complete before any implementation code is written**
3. Data Architect Agent updates `docs/schema/api_contracts.yml` to add both endpoint contract
   entries (included in the same G3 implementation PR — not a follow-on)
4. Chief Engineer Agent authors the source registry migration/seed, `/data-quality` endpoint,
   and `/initial-state` endpoint
5. Implementation PR opens targeting `release/m14` with branch name `feat/m14-g3-{description}`
6. Chief Engineer Agent Step 4 Verify: confirms AC-1 through AC-8 pass against the running
   application using curl or httpx before marking PR ready for review; Data Architect Agent
   confirms AC-9 (`api_contracts.yml` entries present) as part of Step 4 Verify
7. Business PO Step 5 Validate: confirms the analytical intent is satisfied — a JOR scenario's
   `/initial-state` response includes `reserve_coverage_months` with a named IMF source,
   enabling the Persona 2 north star argument (AC-7)

**G3 → G4 gate:** G4's implementation PR must not open until G3 endpoints exist and at least
AC-1 (`/data-quality` JOR 200 response) and AC-6 (`/initial-state` JOR indicator present) pass
in the running application. This is a hard gate per the intent document footer — G4 cannot be
implemented or verified without G3's API layer.

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-06-17
**Sweep period:** G1 sprint exit (2026-06-17) through G3 sprint entry filing (2026-06-17)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| Visual Spec (before/after) section absent from `docs/process/intent-template.md` — surfaced during G1 QA test authorship (PR #1001) when QA Lead had to read `AttributeSelector.tsx` source to resolve a scope ambiguity in AC-6 label scope. Finding logged in insights-log.md 2026-06-17, promoted to GitHub issue #1004. Not a near-miss (template improvement, tracked in issue). | Promoted to issue — not near-miss threshold | No | N/A |
| No findings meeting near-miss threshold in the G1-exit → G3-entry sweep period. | — | No | N/A |

*Sweep period is short (same session as G1 exit). The G1 sprint entry §5 sweep (2026-06-16)
covered the M13-exit → G1-open window. This sweep covers the G1-exit → G3-open window.*

---

## EL Approval Record

**EL approval:** 2026-06-17

> G3 sprint entry approved. All five entry invariants satisfied: release branch exists,
> CI trigger verified, sprint plan EL-approved, ADR-016 Accepted, intent document filed,
> QA tests filed (PR #1011). DA review complete — QA tests confirmed schema-correct against
> ADR-016 API contract; one open item (value field type) flagged for CE to resolve at Step 3.
> Implementation may begin. Chief Engineer Agent may open the G3 implementation PR targeting
> `release/m14` with branch name `feat/m14-g3-{description}`.
> — @PublicEnemage (2026-06-17)
