---
name: m14-g3-sprint-exit
type: sprint-exit
milestone: M14 — Methodology Publication and External Validation
sprint-group: G3
status: Complete
authored-by: PM Agent
date: 2026-06-17
pi-confirmed: true
release-branch: release/m14
sop-reference: docs/process/sprint-planning-sop.md §Sprint Exit Gate
---

# Sprint Exit — M14, G3 (ADR-016 Backend: Source Registry + Data-Quality + Initial-State)

**Status:** Complete — PI Agent confirmation recorded
**Date produced:** 2026-06-17
**Release branch:** `release/m14`
**Sprint entry document:** `docs/process/sprint-plans/m14-g3-sprint-entry.md`

*Authority: `docs/process/sprint-planning-sop.md §Sprint Exit Gate` (Phase B/C output).*

---

## Section 1 — Sprint Identification and Date

| Field | Value |
|---|---|
| Milestone | M14 — Methodology Publication and External Validation |
| Sprint number | G3 |
| Release branch | `release/m14` |
| Sprint groups | G3 |
| Sprint entry document | `docs/process/sprint-plans/m14-g3-sprint-entry.md` |
| Exit checklist issue | #968 |
| Date implementation completed | 2026-06-17 |
| CI status on release branch | Green |

---

## Section 2 — Implementation Status

| Group | PR | Merged? | CI status | Notes |
|---|---|---|---|---|
| G3 — ADR-016 backend: source registry, /data-quality, /initial-state, api_contracts.yml | #1011 | Yes | Green | `release/m14`; all 6 required checks pass |

**Implementation status:** All merged, CI green

**What PR #1011 delivered:**
- Alembic migration `a1b3c5d7e9f2`: creates `entity_data_quality_coverage` table; seeds
  `source_registry` with 5 named sources (CBJ_ANNUAL_2023, IMF_WEO_APR2024,
  DOS_LFS_Q1_2024, IMF_WB_GRC_2010, WORLD_BANK_WDI_2023); upserts JOR
  `simulation_entities` attributes in SA-09 JSONB envelope format; seeds
  `entity_data_quality_coverage` rows for GRC/JOR/EGY/ZMB across Financial, Human
  Development, Ecological, and Governance frameworks
- `app/api/grounding.py`: two ADR-016 endpoints (`/data-quality`, `/initial-state`); SF-1
  and SF-2 empty-response guards
- `app/api/scenarios.py`: `entities: []` guard removed (required for AC-8 fixture)
- `app/main.py`: grounding router registered
- `docs/schema/api_contracts.yml`: full schema entries for both new endpoints (DA RACI
  obligation; AC-9)
- `backend/tests/test_m14_g3_adr016_backend.py`: AC-1–AC-9 pytest+httpx suite (authored
  before implementation per Step 2)

---

## Section 3 — Business PO Acceptance Table

G3 is backend infrastructure — the user-facing surface (Grounding strip) is implemented
in G4. The backend capability itself is validated against the API boundary. The BPO
Step 5 Validate confirms that the analytical intent is satisfied at the data layer — that
a JOR scenario's `/initial-state` response includes `reserve_coverage_months` with a named
IMF/CBJ source, enabling the Persona 2 north star argument.

| Deliverable | Work type | Customer Agent Layer 3 assessment | Business PO verdict | Verdict artifact |
|---|---|---|---|---|
| `/data-quality` endpoint (AC-1–AC-5) + source registry seed | Backend | Filed — intent doc §9 (PASS — endpoint returns `display_name`, named `source_institution`, `data_vintage`, and `confidence_tier`; G4 renders as self-interpreting label; no specialist mediation required) | ACCEPT | `docs/process/intents/M14-G3-2026-06-17-adr016-backend.md §9` |
| `/initial-state` endpoint (AC-6–AC-8) | Backend | Filed — intent doc §9 (PASS — `reserve_coverage_months: 7.1 months · CBJ 2023-Q4 · T2` confirmed in live JOR scenario; ministry analyst can cite CBJ Q4 2023 without translation) | ACCEPT | `docs/process/intents/M14-G3-2026-06-17-adr016-backend.md §9` |
| `api_contracts.yml` update (AC-9) | Documentation | N/A — schema document; not a user-facing indicator output | ACCEPT (schema correct per DA RACI review) | `docs/process/intents/M14-G3-2026-06-17-adr016-backend.md §8` |

**Business PO acceptance status:** All ACCEPT — 2026-06-17

### Notes on Customer Agent Layer 3 assessments

| Deliverable | Serves Persona 2/3/5? | Layer 3 filed before verdict? |
|---|---|---|
| `/data-quality` endpoint | Yes (Persona 2 primary; Persona 3 secondary) | Yes — filed in intent doc §9 before BPO verdict |
| `/initial-state` endpoint | Yes (Persona 2 primary; Persona 3 secondary) | Yes — filed in intent doc §9 before BPO verdict |
| `api_contracts.yml` update | No (schema document; no direct user exposure) | N/A |

**Layer 3 assessment note:** G3 is backend infrastructure — the Layer 3 output (self-
interpreting indicator labels) is produced by G4's Grounding strip rendering logic on
top of G3's JSON response. The Customer Agent Layer 3 assessment in intent doc §9
evaluated the proximate display: "Reserve coverage: 7.1 months · CBJ 2023-Q4 · T2"
(the format G4 will render per ADR-016 §Component 2 API contract). The assessment
confirmed PASS: source name (CBJ), vintage (2023-Q4), and tier (T2) are all human-
readable and require no specialist mediation for Persona 2.

**BPO validation method:** `curl` against running `worldsim-api-1` Docker container;
JOR scenario `68b31277` created and run via `POST /scenarios` + `POST /scenarios/{id}/run`
during BPO Step 5 session (2026-06-17). All 9 ACs confirmed in the live application.

**BPO observations:**
- AC-7 (north star indicator): `reserve_coverage_months: 7.1 · source: "CBJ" · vintage: "2023-Q4" · confidence_tier: 2` — primary citation confirmed in live JOR scenario response ✅
- Source is CBJ (Central Bank of Jordan) — more authoritative than the IMF BOP example in the intent doc's illustrative schema (CBJ is the primary source; IMF BOP derives from it). Positive deviation from example. ✅
- AC-2 (ZMB synthetic): `is_synthetic: true`, `synthetic_basis: "SADC comparable economies 2022-2023"` — Zambian analyst sees transparent synthetic basis ✅
- AC-5 and AC-8 (SF-1/SF-2 guards): unsupported entity and pre-G3 scenario both return HTTP 200 with empty structures — no silent 404 or 500 failure ✅

**North star check (P-7, backend layer):** After G3, `GET /api/v1/scenarios/{jor_id}/initial-state`
returns `reserve_coverage_months` with `source: "CBJ"` and `vintage: "2023-Q4"` for a
completed JOR scenario. This is the data layer that enables the Persona 2 argument:
"The model uses Jordan's reserve coverage as reported by the Central Bank of Jordan —
7.1 months as of Q4 2023. That figure is Tier 2 confidence — observed data. Here is
our source." Full P-7 (screen-visible, within-90-seconds) requires G4 to land on top
of G3. G3's P-7 obligation at the API layer is satisfied. North star check: PASS at
backend layer; forward trace to G4.

**Step 4 observation (not a rejection):** The G3 migration was not pre-applied at
initial probe — endpoint returned HTTP 500 (`UndefinedTableError`) until
`alembic upgrade head` was run. The implementing agent's commit noted `ruff check . ✓`
and `mypy app/ ✓` but did not include a live endpoint probe as Step 4 evidence. Noted
in intent doc §8 as a Step 4 discipline observation: future backend sprints with schema
migrations should include `alembic upgrade head` + live endpoint probe explicitly in
the Step 4 pre-verification sequence. Not a rejection — CI would catch this; recorded
as an institutional learning note, not a near-miss threshold event.

---

## Section 4 — Open Rejections

No open rejections. Proceed to Section 5.

---

## Section 5 — PI Agent Sprint Exit Confirmation

**Exit conditions checklist (PI Agent):**

- [x] All implementation groups merged; CI green on release branch — PR #1011 merged to
  `release/m14`; PR #1012 (BPO accept artifact) merged to `release/m14`; CI green on both
- [x] Business PO ACCEPT verdict filed for each user-facing deliverable — ACCEPT on record for
  `/data-quality` and `/initial-state` endpoints in intent doc §9; filed 2026-06-17
- [x] Customer Agent Layer 3 assessment on record for all Persona 2/3/5 deliverables, filed
  before Business PO verdict — Layer 3 assessment filed in intent doc §9 before BPO verdict
  (proximate assessment: "Reserve coverage: 7.1 months · CBJ 2023-Q4 · T2")
- [x] No open rejection artifacts — confirmed; no REJECT artifacts exist for G3
- [x] Near-miss entry for each rejection — no rejections in G3; no near-miss obligation from
  rejections

**G4 gate confirmed open:** AC-1 (`/data-quality` JOR → 200) and AC-6 (`/initial-state`
JOR indicator present) both confirmed in the running application during BPO Step 5.
Per intent doc §3 footer: "G4 implementation PR may now open." G3 is a hard prerequisite
for G4 — this gate is now satisfied.

**G4 forwarded observation:** The `/initial-state` endpoint includes a `"None"` framework
key for legacy simulation attributes lacking a `measurement_framework` field in their SA-09
envelope. G4's Grounding strip must filter to named framework keys (financial,
human_development, ecological, governance, political_economy) only. This is a display-
layer concern — not a G3 defect.

**PI Agent sprint exit verdict:** Confirmed — all exit conditions satisfied

**PI Agent confirmation:**

> G3 sprint exit conditions are satisfied as of 2026-06-17. Implementation (PR #1011) and
> BPO accept artifact (PR #1012) are both merged to `release/m14` with CI green. Business PO
> ACCEPT verdict is filed for all G3 deliverables (`/data-quality` and `/initial-state`
> endpoints, source registry seed) with Customer Agent Layer 3 assessment on record prior to
> each verdict. No rejection artifacts exist. Step 4 observation (migration not pre-applied at
> initial probe) is recorded as an institutional discipline note — not a near-miss threshold
> event. G4 gate is open: AC-1 and AC-6 confirmed in the running application.
>
> G3 is closed. G4 sprint entry may now be filed.

---

## Sprint Exit Artifact Statement

This document is the sprint exit artifact for G3 of M14. It supersedes any informal exit
notation in SESSION_STATE.md for this sprint. Filed at
`docs/process/sprint-plans/m14-g3-sprint-exit.md`.
