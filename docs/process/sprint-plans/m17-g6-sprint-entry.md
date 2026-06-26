---
name: m17-g6-sprint-entry
type: sprint-entry
milestone: M17 — Calibration and Comparative Infrastructure
sprint-group: G6 — Process and Transparency Documents
status: Awaiting EL approval — implementation blocked
authored-by: PM Agent
authored-date: 2026-06-26
el-approved: pending
release-branch: release/m17
sop-reference: docs/process/sprint-planning-sop.md
---

# Sprint Entry — M17, G6: Process and Transparency Documents

**Status:** Awaiting EL approval — implementation blocked
**Date authored:** 2026-06-26
**Release branch:** `release/m17`
**Sprint plan:** `docs/process/sprint-plans/m17-sprint-plan.md` (EL Approved 2026-06-25)

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).
G6 covers two documentation issues with no production code changes: #1276 (governance horizon
disclosure — UI text addition to Zone 1D) and #1277 (sprint-planning-sop.md UX/UI design
artifact gate amendment). Both are derived from the M17-G1 CM Governance Sensitivity
Specification and the HORIZON sweep insight log promotion. Implementation may not begin
on either issue until this entry is EL-approved.*

*Sprint classification: both issues are documentation/process changes. Neither introduces a
new zone, data contract, or simulation module. #1276 is a UI text addition (No False Precision
principle); #1277 is a process document amendment (SOP improvement). Neither requires BPO
acceptance or Customer Agent Layer 3 assessment.*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M17 — Calibration and Comparative Infrastructure |
| GitHub Milestone | #18 |
| Sprint group | G6 — Process and Transparency Documents |
| Release branch | `release/m17` |
| Sprint plan document | `docs/process/sprint-plans/m17-sprint-plan.md` |
| Exit checklist issue | #982 |
| Sprint groups in scope | G6 only |
| Issues in scope | #1276, #1277 |
| ADR gate | N/A — documentation amendments within existing architecture; no structural decisions |
| Implementing agents | UX Designer (#1276 — placement confirmation + text); PM Agent (#1277 — SOP amendment) |
| Wave | Wave 2 (Wave 1 exit confirmed 2026-06-25) |
| Demo dependency | #1276 must be present before Demo 7 live session (#843, M18) is scheduled |
| Sequencing | Capacity-allowing — runs after G5 exit confirmation (2026-06-26); no dependency on #1275 |

**Issue classification summary:**

| Issue | Title | Classification | BPO acceptance required? |
|---|---|---|---|
| #1276 | docs(zone-1d): governance horizon disclosure | Documentation / UI text — No False Precision transparency disclosure | No — transparency text, not a persona-impacting feature or layout change |
| #1277 | docs(process): sprint-planning-sop.md UX/UI design artifact gate | Process document amendment | No — internal process improvement; no user-facing change |

---

## Section 2 — Entry Invariants Checklist

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m17` cut from `main` 2026-06-25 (commit d806957)
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes
  `release/m*` — confirmed at M17 kickoff 2026-06-25.
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m17-sprint-plan.md`
  `el-approved: 2026-06-25`
- [x] **Wave 1 exit gate confirmed:** G1 sprint exit at `docs/process/sprint-plans/m17-g1-sprint-exit.md`;
  PI Agent confirmation 2026-06-25

**Structural gates: CLEAR.**

### 2.2 — ADR prerequisite gate

Neither G6 issue introduces a new architectural decision:

- **#1276** (governance horizon disclosure): UI text addition — a `<span>` or tooltip in Zone 1D.
  No new zone, no new component boundary, no data contract change. ADR-017 Zone 1D boundaries
  are unchanged. No ADR required.

- **#1277** (SOP amendment): text addition to a process document. No code change, no schema
  change, no architectural decision. No ADR required.

**ADR prerequisite status: CLEAR** — no new ADR required for either issue.

### 2.3 — Intent document gate

**#1276:** The CM-specified disclosure text is authoritative and quoted in the issue body.
UX Designer must confirm placement (Zone 1D attestation section vs. GOV composite label tooltip)
before the implementation PR opens. Placement confirmation counts as the intent-equivalent
for this issue — no separate intent document required given the single-paragraph scope.

**Placement candidates (UX Designer to select one before PR opens):**
- A — Static one-line note in Zone 1D attestation section below the governance composite row
  (always visible, no interaction required; L0 per UX Architectural Commitment 2)
- B — Tooltip on the GOV composite label (hover/tap to reveal; L1 — acceptable for
  supplementary methodology text per `docs/ux/information-hierarchy.md`)
- C — Demo walkthrough narration text only (no in-app change; acceptable only if EL agrees
  the disclosure is sufficient outside the running application)

**UX Designer must record placement decision as a comment on #1276 before the PR opens.**
If UX Designer is not activated in the implementing session, the implementing agent defaults
to Placement A (always-visible attestation note) — the most conservative interpretation of
UX Architectural Commitment 2 (no specialist interaction required to see primary methodology
disclosures).

**#1277:** The issue body specifies the full amendment — seven components. PM Agent holds R on
`docs/process/sprint-planning-sop.md`. No separate intent document required; the issue body
is the specification.

**Intent document gate: SATISFIED** — CM text on record for #1276; issue body is specification
for #1277; UX placement confirmation required before #1276 PR opens.

### 2.4 — QA / test gate

**#1276 (UI text):**
The disclosure text must be present in the running application (or in the demo narration per
Placement C). No E2E test is required for static methodology disclosure text — testing would
assert the string content of a span, which provides no additional quality signal beyond CI
lint. The implementing agent must confirm in the PR description that the text is visible in the
running UI and match the CM-specified disclosure exactly.

**#1277 (SOP document):**
No QA test applies to a process document amendment. The implementing agent confirms the
amendment is complete by verifying all seven specified components appear in the committed file.

**QA gate: SATISFIED** — documentation-only sprint; no new test files required.

### 2.5 — UX / design gate

**#1276** has a UX placement decision (see §2.3). Placement A (attestation section) does not
require a mockup — it is a text-only addition to an existing layout section. If Placement B
(tooltip) is selected, the UX Designer must confirm the interaction pattern does not violate
UX Architectural Commitment 2 before the PR opens.

**#1277** has no UX implication — process document only.

**UX gate: CLEAR** with the Placement A default assumption.

---

## Section 3 — Issue-by-Issue Implementation Scope

### #1276 — Governance horizon disclosure

**File(s) to modify:** The component rendering Zone 1D attestation or the GOV composite label.
UX Designer confirms the exact file. Likely `frontend/src/components/` — Zone 1D component.

**Required text (CM-specified — must appear verbatim or with approved paraphrase):**
> "Governance indicators (rule of law, democratic quality) respond to fiscal adjustment over
> 3–6 year horizons in this model's calibration. An 8-step quarterly window captures the
> beginning of the governance stress trajectory; full divergence requires a 12–24 step analysis."

**Pre-push gate:** `cd frontend && npm run build` — mandatory (frontend/src/ change).

**PR target:** `release/m17`

### #1277 — sprint-planning-sop.md UX/UI design artifact gate

**File(s) to modify:** `docs/process/sprint-planning-sop.md`

**Amendment components (all seven required per issue body):**
1. Classification trigger definition
2. Minimum artifact — UX mockups requirement
3. Conditional artifact — UI mockups (when required)
4. Panel composition (five named agents)
5. Panel review format (GitHub comment + tag PM Agent)
6. Binding specification rule (intent doc references panel-approved mockups)
7. Panel review fail condition (REJECT blocks BPO acceptance; PI Agent blocks architecture phase)

**Pre-push gate:** No backend or frontend changes — lint gate not triggered. Conventional Commits
format required.

**PR target:** `release/m17`

---

## Section 4 — Exit Conditions

G6 exits when:

1. Both PRs merged to `release/m17` with CI green
2. #1276: disclosure text present in the running application, exact match to CM-specified text
   confirmed in PR description
3. #1277: all seven SOP components present in `docs/process/sprint-planning-sop.md`,
   confirmed by PM Agent in PR description
4. Issues #1276 and #1277 closed
5. PI Agent sprint exit confirmation filed

BPO acceptance is not required for either deliverable (documentation/process classification).
Customer Agent Layer 3 assessment is not required (neither issue serves Personas 2, 3, or 5
as a direct capability).

North star test: not required for this sprint — no user-facing capability change. #1276 is
a transparency disclosure that serves all personas but is not a new analytical capability.
Infrastructure sprint classification applies.

---

*Intent document authority: EL decision 2026-06-26 (proceed with #1276 and #1277 in same
sprint group). Issues: #1276 (governance horizon disclosure), #1277 (sprint-planning-sop.md
amendment). Implementing agents: UX Designer (#1276), PM Agent (#1277). Pre-push gate:
frontend build for #1276 (frontend/src/ change); no gate for #1277 (docs only).*
