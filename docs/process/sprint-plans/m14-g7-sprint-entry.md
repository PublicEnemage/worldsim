---
name: m14-g7-sprint-entry
type: sprint-entry
milestone: M14 — Methodology Publication and External Validation
sprint-group: G7
status: Filed — awaiting EL approval
authored-by: PM Agent
authored-date: 2026-06-18
el-approved: 2026-06-18
release-branch: release/m14
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M14, G7: Governance and Onboarding Documentation

**Status:** EL Approved — 2026-06-18
**Date authored:** 2026-06-18
**Release branch:** `release/m14`
**Sprint plan:** `docs/process/sprint-plans/m14-sprint-plan.md` (EL Approved 2026-06-16)

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).
G7 is the governance and onboarding documentation group. It carries no ADR prerequisite
and no sequencing dependency on G3/G4/G5/G6 — it may proceed in parallel. Issues in agent
scope: #988 (Goodhart's Law mitigation framework) and #989 (global south analyst onboarding
documentation suite). EL-action items #3 (TSC formation) and #6 (branch protection bypass
restriction restoration) are governance decisions outside agent implementation scope; no intent
document is required for them. Implementing agent: PM Agent.*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M14 — Methodology Publication and External Validation |
| GitHub Milestone | #15 |
| Sprint group | G7 — Governance and Onboarding Documentation |
| Release branch | `release/m14` |
| Sprint plan document | `docs/process/sprint-plans/m14-sprint-plan.md` |
| Exit checklist issue | #968 |
| Sprint groups in scope | G7 only |
| ADR gate | None — documentation/governance sprint; no ADR required |
| Implementing agent | PM Agent |

---

## Section 2 — Entry Invariants Checklist

*All items must be checked before any implementation PR is opened for G7.
An unchecked invariant blocks implementation from beginning.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m14` cut from `main` 2026-06-16
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes
  `release/m*` — confirmed 2026-06-16 (Ruleset ID 17751852 with 6 required checks: `changes`,
  `lint`, `test-backend`, `playwright-e2e`, `compliance-scan`, `branch-naming`)
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m14-sprint-plan.md`
  `el-approved: 2026-06-16`

### 2.2 — ADR prerequisite gate

G7 is a documentation and governance sprint group. No ADR gates any of its deliverables.
The Goodhart's Law mitigation framework (#988) is a PM Agent–authored governance document;
it becomes the TSC's founding mandate document upon EL review and does not require its own ADR.
The onboarding suite (#989) documents existing platform capabilities; it does not introduce
new architectural decisions.

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| G7 | None | N/A — documentation sprint | CLEAR |

- [x] No ADR prerequisite applies to G7. Gate is clear.

### 2.3 — Intent document gate

*An intent document must be filed before any G7 implementation PR opens.
(Authority: docs/process/agent-execution-lifecycle.md Step 1)*

**Sequencing note:** The intent document and QA test file were authored on 2026-06-18 before
this sprint entry was filed. This is permitted per docs/process/agent-execution-lifecycle.md Step 1:
"The implementing agent may not open any PR until (1) the sprint entry document is filed and
EL-approved." No implementation PR has been opened. The intent document §0 contains an explicit
PI Agent anticipatory near-miss flag covering this sequence. Filing this sprint entry document
and obtaining EL approval is the remaining gate before any implementation PR opens.

- [x] Intent document filed for all G7 agent-scope deliverables

| Deliverable | ADR reference | Intent document path | Filed? |
|---|---|---|---|
| Onboarding documentation suite (#989) — quick-start, scenario-creation, methodology-overview, data-provenance | None (docs sprint) | `docs/process/intents/M14-G7-2026-06-18-governance-onboarding.md` | ✅ Filed 2026-06-18 |
| Goodhart's Law mitigation framework (#988) | None (docs sprint) | `docs/process/intents/M14-G7-2026-06-18-governance-onboarding.md` | ✅ Filed 2026-06-18 (same intent doc) |

**EL-action items explicitly excluded from intent coverage:**
- #3 — TSC formation: EL establishes Technical Steering Committee governance structure.
  The PM Agent authors the Goodhart's Law framework draft (#988) for EL review; EL assumes
  ownership before G7 exits. TSC formation itself is an EL governance action — no intent
  document required.
- #6 — Branch protection bypass restriction restoration: blocked on #3 Stage 2 completion.
  No agent deliverable; EL action when second governance account is in place.

### 2.4 — QA test authorship gate

*For G7 documentation deliverables, QA tests take the form of file-system checks and manual
timed-navigation criteria. No Playwright test suite is required; the acceptance criteria are
content-presence checks (grep equivalents) and one BPO timed navigation.
(Authority: docs/process/agent-execution-lifecycle.md Step 2; intent document §7)*

- [x] QA test file authored before any G7 implementation PR opens

| Deliverable | Intent document | Test file path | Authored before implementation? |
|---|---|---|---|
| Onboarding suite + Goodhart's Law framework | `docs/process/intents/M14-G7-2026-06-18-governance-onboarding.md` | `backend/tests/test_m14_g7_governance_onboarding.py` | ✅ Yes — authored 2026-06-18; 28 tests covering AC-1–AC-6; AC-7 marked `pytest.mark.skip` (BPO timed navigation) |

**QA test notes:**
- AC-1 through AC-6: pytest file-system checks (grep equivalents for all automatable
  string-presence criteria — `Zone 1B`, `MDA alert`, `grounding strip`, `STRUCTURAL_ABSENCE`,
  four-section keyword checks for the Goodhart's Law framework)
- AC-4 automated test confirms ≥1 named blindspot; BPO confirms ≥3 named blindspots at Step 5
- AC-6 four-section check: per-section keyword presence; BPO confirms operational specificity
  (gaming definition names a specific WorldSim parameter; TSC obligations are named, not aspirational)
- AC-7 (BPO timed navigation, 5-minute ceiling): marked `pytest.mark.skip` — executed by
  Business PO proxy at Step 5 Validate

---

## Section 3 — Scope Declaration

### 3.1 — Issues in scope

| Issue | Title | Group | Priority |
|---|---|---|---|
| #989 | Global south analyst onboarding documentation | G7 | immediate |
| #988 | Goodhart's Law mitigation framework | G7 | immediate |

**EL-action items on the M14 board, out of agent implementation scope:**

| Issue | Title | Disposition |
|---|---|---|
| #3 | TSC formation | EL governance action — no agent deliverable |
| #6 | Branch protection bypass restriction restoration | Blocked on #3 Stage 2; no agent deliverable |

### 3.2 — G7 deliverables

**#989 — Onboarding documentation suite (four files):**

| File | Required content marker | Primary AC |
|---|---|---|
| `docs/onboarding/quick-start.md` | "Zone 1B" + "MDA alert" in instrument cluster reading instructions | AC-1, AC-2 |
| `docs/onboarding/scenario-creation.md` | "grounding strip" + confidence tier number explanation | AC-3 |
| `docs/onboarding/methodology-overview.md` | ≥3 named model blindspots (not generic disclaimers) | AC-4 |
| `docs/onboarding/data-provenance.md` | "STRUCTURAL_ABSENCE" in a worked negotiation example | AC-5 |

**#988 — Goodhart's Law mitigation framework:**

| File | Required content | Primary AC |
|---|---|---|
| `docs/governance/goodharts-law-mitigation.md` | Four sections: gaming definition naming ≥1 specific parameter; parameter range signals; TSC named monitoring obligations; open-source audit pathway | AC-6 |

**README.md update:**
`README.md` must contain a link to `docs/onboarding/quick-start.md` under a "Getting Started"
(or equivalent) section heading — the anchor point for BPO navigation validation (AC-1, AC-7).

**North star obligation (intent §2 P-7):**
After G7, a Zambian debt management analyst referred to WorldSim after Demo 5 can open
`README.md`, follow the quick-start guide, and within 10 minutes have loaded a Jordan scenario,
identified "Reserve coverage TERMINAL breach" in Zone 1B, and understood what "Tier 2 · IMF BOP
2024-Q1" means for her negotiating position — without requiring Engineering Lead mediation.

### 3.3 — Issues explicitly out of scope

| Issue | Title | Horizon | Rationale for exclusion |
|---|---|---|---|
| All G5 items | ADR-015 Evidence Thread Architecture | Complete | G5 COMPLETE 2026-06-18 |
| All G6 items | Methodology, calibration, instrument legibility | In progress (parallel) | G6 sprint entry filed 2026-06-18; separate parallel group |
| All G6b items | Path 2 design groundwork | In progress (parallel) | G6b intent filed 2026-06-18; design artifacts only |
| All G6c items | Zone 1A Phase 1 design thinking | In progress (parallel) | G6c intent filed 2026-06-18; design-only |
| #843 | Live stakeholder demo (Demo 5) | M14 closure gate | G8 scope — M14 exit gate |
| Video tutorials, localization | Out of scope | Future milestone | English documentation files only; no video or translated content |
| Developer / API documentation | Out of scope | Not this sprint | `docs/CONTRIBUTING.md` and `docs/schema/` serve Persona 4; G7 serves Persona 2 |
| ADR-016 Component 4 (Path 2 data upload) | Out of scope | M16 | Scenario creation guide covers grounding strip (ADR-016 Components 1–3) only |

---

## Section 4 — ADR Prerequisite Summary

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| G7 | None | N/A — documentation and governance sprint | After EL approval of this entry document |

**Implementation sequencing for G7:**

1. EL approves this entry document (this step)
2. PM Agent opens implementation PR targeting `release/m14` with branch name
   `feat/m14-g7-governance-onboarding` and creates the following files:
   - `docs/onboarding/quick-start.md`
   - `docs/onboarding/scenario-creation.md`
   - `docs/onboarding/methodology-overview.md`
   - `docs/onboarding/data-provenance.md`
   - `docs/governance/goodharts-law-mitigation.md`
   - `README.md` updated with "Getting Started" link to quick-start
3. PM Agent Step 4 Verify: runs AC-1–AC-6 shell checks against the committed documents;
   confirms all string-presence criteria pass; records verdict in intent doc §8
4. Business PO Step 5 Validate:
   - Customer Agent Layer 3 assessment on record (G7 is a Persona 2–serving capability)
   - BPO executes AC-7 timed navigation (README → quick-start → Tier 2 explanation, ≤5 minutes)
   - BPO confirms north star scenario (P-7): Zambian analyst reaches working proficiency within
     10-minute ceiling from README entry point
   - BPO records ACCEPT or REJECT verdict in intent doc §9

---

## Section 5 — Near-Miss Sweep

**Near-miss sweep date:** 2026-06-18
**Sweep period:** G5 sprint exit (2026-06-18) through G7 sprint entry filing (2026-06-18)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| Intent document (Step 1) and QA tests (Step 2) for G7 were authored on 2026-06-18 before this sprint entry document was filed. No implementation PR was opened; the intent doc §0 contains an explicit anticipatory gate note from the PI Agent. The standard process order (sprint entry → intent → QA → impl) was inverted for Steps 1 and 2, but the hard gate (no impl PR without filed entry) was not crossed. Finding: benign sequence variance, not a near-miss — the gate that prevents harm (no impl PR) was respected. | Process sequence variance — no gate crossed | No — gate was not crossed; no NM warranted | N/A |

*No additional process gaps identified in the sweep period.*

---

## EL Approval Record

**EL approval:** 2026-06-18

> G7 sprint entry approved. All entry invariants satisfied: release branch exists, CI trigger
> verified, sprint plan EL-approved, no ADR gate (documentation sprint), intent document filed
> 2026-06-18, QA tests filed 2026-06-18. Sequencing note acknowledged — intent and QA tests
> were authored before the sprint entry, but no implementation PR was opened; the hard gate was
> respected. Implementation is unblocked. PM Agent may open the implementation PR
> `feat/m14-g7-governance-onboarding` targeting `release/m14`.
> — @PublicEnemage (2026-06-18)
