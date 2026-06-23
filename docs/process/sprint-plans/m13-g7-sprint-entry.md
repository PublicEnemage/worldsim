---
name: m13-g7-sprint-entry
type: sprint-entry
milestone: M13 — Political Economy and Instrument Credibility
sprint-group: G7
status: Filed — awaiting EL approval before implementation begins
authored-by: PM Agent
authored-date: 2026-06-12
el-approved: false
release-branch: release/m13
sop-reference: docs/process/sprint-planning-sop.md
adr-gate: ADR-014 — ACCEPTED 2026-06-12 (PR #926)
---

# Sprint Entry — M13, G7: Alert Panel Master-Detail UX

**Status:** Filed — awaiting EL approval before implementation begins
**Date authored:** 2026-06-12
**Release branch:** `release/m13`
**Sprint plan:** `docs/process/sprint-plans/m13-sprint-plan.md`

*Authority: `docs/process/sprint-planning-sop.md §Sprint Entry Gate` (Phase C output).
This document gates G7 specifically. The M13 Sprint 1 entry (`m13-sprint-1-entry.md`)
listed G7 as `BLOCKED_ADR`. ADR-014 was accepted 2026-06-12 (PR #926); this entry
document satisfies the unblock condition stated in the Sprint 1 entry before
implementation may begin.*

---

## Section 1 — Sprint Identification

| Field | Value |
|---|---|
| Milestone | M13 — Political Economy and Instrument Credibility |
| GitHub Milestone | #9 |
| Sprint number | 1 (Wave 3 — G7 unblock entry) |
| Release branch | `release/m13` |
| Sprint plan document | `docs/process/sprint-plans/m13-sprint-plan.md` |
| Exit checklist issue | #264 |
| Sprint groups in scope | G7 only |
| ADR gate cleared | ADR-014 — ACCEPTED 2026-06-12 (PR #926) |
| Implementing agent | Frontend Architect Agent (per ADR-014 panel) |

---

## Section 2 — Entry Invariants Checklist

*All items must be checked before any implementation PR is opened for G7.
An unchecked invariant blocks implementation from beginning.*

### 2.1 — Structural gates

- [x] **Release branch exists:** `release/m13` cut from `main` 2026-06-12 (verified in M13 Sprint 1 entry)
- [x] **CI trigger verified:** `.github/workflows/ci.yml` `pull_request: branches` includes
  `release/m*` — confirmed at M13 kickoff (pre-existing NM-035 fix)
- [x] **Sprint plan EL-approved:** `docs/process/sprint-plans/m13-sprint-plan.md` approved 2026-06-12

### 2.2 — ADR prerequisite gate

The M13 Sprint 1 entry listed G7 as `BLOCKED_ADR` (alert panel ADR PENDING_NUMBER). ADR-014
was authored, accepted, and merged 2026-06-12. This gate is now CLEAR.

| Group | Required ADR | ADR status | Gate |
|---|---|---|---|
| G7 | ADR-014 — alert panel master-detail | ACCEPTED 2026-06-12 (PR #926) | **CLEAR** |

- [x] G7's ADR prerequisite is satisfied. ADR-014 status: `Accepted`.

### 2.3 — Intent document gate

*Intent document must be filed at `docs/process/intents/ADR-014-YYYY-MM-DD-alert-panel-ux.md`
before any G7 implementation PR opens.*
*(Authority: docs/process/agent-execution-lifecycle.md Step 1)*

- [ ] Intent document filed for G7 alert panel UX deliverable — **BLOCKING IMPLEMENTATION**

| Deliverable | ADR reference | Intent document path | Filed? |
|---|---|---|---|
| G7 — Alert panel Zone 1B persistent-detail (#852) | ADR-014 | `docs/process/intents/ADR-014-2026-06-12-alert-panel-ux.md` | No — must file before G7 PR opens |

**Three mandatory elements from UX Designer conditional sign-off (ADR-014 §UX Implication Statement):**
The intent document must include explicit specification for all three UX Designer sign-off
conditions before any implementation PR opens. A G7 PR opened without these in the intent
document is a process violation.

1. **Compact row height constraint** — max 26px per row (single-line truncated) to preserve
   "top 1–3 visible without scroll" at 1024×768 minimum viewport
   (Reference: UX-1 / `docs/ux/information-hierarchy.md §1B`)
2. **Mode-dependent tense in detail slot** — explicit specification of how "BREACHED" / "N%
   above floor" status language is mode-contextualized per `information-hierarchy.md §1B`
   ("Alert tense is mode-dependent") (Reference: UX-2)
3. **Compact row cohort omission** — explicit documentation that compact rows are exempt from
   `information-hierarchy.md §1B` "top affected cohort" requirement, with rationale. Ruling
   already recorded in ADR-014: compact rows are a severity-rank scan surface, not an evidence
   surface. Intent document must document the deviation and cite the ruling. (Reference: UX-7)

**Section 5 additional intent document requirements:** The alert interaction lifecycle and
collision panel deliberation (Section 5 below) resolves specifications across six scope
questions. See §5.2 PM Agent Ruling Summary for resolved items and §5.5 for deferred items.
All resolved Q1–Q4 specifications, plus the Q1 population data availability determination
and Q4 memoisation boundary (Frontend Architect additions), must appear in the intent document.

### 2.4 — QA test authorship gate

*QA tests must be authored from the intent document's acceptance criteria before implementation
code is written.*
*(Authority: docs/process/agent-execution-lifecycle.md Step 2)*

- [ ] QA test file authored for G7 before implementation begins — **BLOCKING IMPLEMENTATION**

| Deliverable | Intent document | Test file path | Authored before implementation? |
|---|---|---|---|
| G7 — Alert panel (#852) | `docs/process/intents/ADR-014-2026-06-12-alert-panel-ux.md` | `frontend/tests/` — Zone 1B Playwright spec | No — must be authored after intent document is filed, before implementation PR opens |

**Required test coverage (from ADR-014 acceptance criteria and silent failure modes):**

The QA Lead authors tests covering the four observable application states from the ADR:

- **UX-3 acceptance criterion:** Playwright — Greece 2012 fixture at step 4; assert
  `data-testid="zone-1b-top-detail"` is visible within Zone 1B bounds, `detail-indicator-name`
  non-empty, `detail-current-value` non-empty numeric — no click or scroll between fixture
  load and assertion
- **UX-6 acceptance criterion:** Playwright — fixture with ≥1 TERMINAL alert; assert
  `data-testid="zone-1b-top-detail"` has `data-severity="TERMINAL"` and is visible at 1440×900
  without any click or scroll events; bounding-box assertion confirms within Zone 1B bounds
- **Silent failure 1:** Assert `data-testid="zone-1b-top-detail"` has `clientHeight > 0`
  immediately after fixture load at 1024×768, 1280×800, and 1440×900 — no user interactions
- **Silent failure 2:** Advance scenario one step; assert `data-testid="detail-consecutive"`
  text matches current step's `consecutive_breach_steps` for the top-ranked alert
- **Silent failure 3:** Assert no compact row (`data-testid="compact-alert-row"`) has cursor
  style other than `default`; assert clicking a compact row produces no change to
  `data-testid="zone-1b-top-detail"` content
- **Silent failure 4 (Mode 3):** Fire a control input causing a new highest-severity alert;
  assert `data-testid="detail-new-badge"` is present and visible before any user interaction

---

## Section 3 — Scope Declaration

### 3.1 — Issues in scope

| Issue | Title | Group | Priority |
|---|---|---|---|
| #852 | ux: alert panel (Zone 1B) needs master-detail layout | G7 | near-term |

### 3.2 — Issues explicitly out of scope

All other M13 issues are either complete (G1–G6) or in the near-term backlog. No
additional issues are being added to G7. Alert panel scope is bounded by ADR-014:
Zone 1B persistent-detail + scan-only compact list layout. Per-cohort income disaggregation
beyond the `cohort` subheader field, full provenance disclosure, and sparkline are
explicitly excluded from G7 per ADR-014 §Known Limitations and §Detail Slot Content.

| Issue | Rationale for exclusion |
|---|---|
| #22, #35, #102, #271, #274, #393, #394, #823, #824, #837 | Near-term backlog — not in any wave; revisit at M13 midpoint HORIZON sweep |

---

## Section 4 — ADR Prerequisite Summary

| Group | ADR required | ADR status | Implementation may begin? |
|---|---|---|---|
| G7 | ADR-014 | ACCEPTED 2026-06-12 (PR #926) | **Yes — after EL approves this entry document, intent document is filed, and QA tests are authored** |

**Implementation sequencing for G7:**
1. EL approves this entry document (this step)
2. Frontend Architect Agent authors intent document at `docs/process/intents/ADR-014-2026-06-12-alert-panel-ux.md` — must include all three UX Designer sign-off conditions
3. QA Lead authors test file before implementation PR opens
4. Implementation PR opens targeting `release/m13`
5. Viewport verification required before PR is marked ready for review (per ADR-014 §Height Budget): actual Zone 1B computed height at 1024×768, 1280×800, and 1440×900 must be measured and confirmed
6. Business PO Step 5 Validate and Customer Agent Layer 3 assessment required before sprint exit

---

## Section 5 — Alert Interaction Lifecycle and Collision Scope Declaration

*Panel deliberation: 2026-06-12 (amended). Supersedes the four-question four-agent deliberation
filed in PR #933. Panel expanded to five agents; scope expanded to six questions per EL review
of the G7 sprint entry.*

*Panel: Design Thinking Agent, Development Economist Agent, Chief Methodologist Agent, UX Designer
Agent, Frontend Architect Agent. PM Agent synthesises into rulings. Each ruling is either "resolved
in G7 with stated specification" or "explicitly deferred with rationale and follow-on ADR reference."*

*Purpose: Six pre-implementation scope gaps identified during EL review. Each gap left unresolved
would require scope negotiation during implementation — the highest-cost resolution moment. Rulings
from resolved questions become mandatory intent document specifications. Rulings from deferred
questions become follow-on ADR references and must not be implemented in G7 without a new ADR.*

*EL endorsement of these rulings is required alongside sprint entry approval. A ruling marked
"resolved in G7" that is subsequently challenged mid-implementation returns to this panel — it
does not unilaterally narrow.*

---

### 5.1 — Panel Deliberation

---

#### Question 1: Alert deduplication — same indicator, multiple entities at the same step

*Context: In the Hormuz scenario, both JOR and EGY breach reserve_coverage_months TERMINAL at
step 3. Both appear as separate rows in `mda_alerts`. ADR-014's ranking rule specifies (severity
DESC, step_index ASC) but does not name a tiebreak when two alerts share both fields. Design
Thinking question: does the analyst experience these as one crisis or two independent findings?*

**Design Thinking Agent:**
The analyst's mental model in a multi-entity geopolitical scenario is entity-contextualised
throughout: she tracks Jordan and Egypt as two sovereign actors with separate policy levers,
separate domestic politics, and separate negotiating positions. A merged "JOR + EGY" alert
collapses this distinction into a regional aggregate that maps to no specific negotiating
position — the relevant question at the table is "what can Jordan's finance ministry do?",
not "what can the Hormuz region do?" The deduplication impulse comes from visual-clutter
concern, but the compact list's "+N more ↕" pattern already handles clutter correctly. The
tiebreak question (which entity occupies the detail slot) must be deterministic and
semantically motivated — not alphabetical, not insertion-order. Entity population satisfies
this requirement because it aligns with the human cost priority that governs the rest of the
instrument.

**Development Economist Agent:**
Jordan's 5.1 million population and Egypt's 104 million are not interchangeable. Collapsing a
dual-entity TERMINAL breach into a single deduplicated row suppresses a 20× magnitude
asymmetry in the human cost of the same reserve drawdown. The finance minister's analyst
needs both to be visible because the negotiating argument runs on two tracks: severity of the
breach and scale of the population bearing the cost. If forced to choose one for the detail
slot, the larger-population entity's alert is the stronger argument — it names more people
facing intergenerational consequences. Do not deduplicate.

**Chief Methodologist Agent:**
JOR reserve_coverage_months and EGY reserve_coverage_months are independent statistical
observations with independent confidence tiers and independent data provenance — one may be
Tier 2 (IMF Article IV, recent vintage); the other Tier 3 (synthetic comparable). A
deduplicated "JOR + EGY" alert requires a composite confidence tier that is not a defined
statistical operation in this framework. More fundamentally: within a tiebreak between two
alerts sharing (severity, step_index), the higher-confidence alert (lower tier number) is
the stronger evidentiary claim and ranks first — this is the methodologist's primary tiebreak;
entity population size is the secondary tiebreak for cases where confidence tier is also equal.

**UX Designer Agent:**
`information-hierarchy.md §1B` requires entity identity in Zone 1B alert rows — removing it
through deduplication is a §1B content violation. The multi-entity tiebreak is an unspecified
case in ADR-014 §Top-Alert Ranking Rule (written against single-entity examples); it must be
closed in the G7 intent document as a ranking rule extension. Because the extension fills an
unspecified case rather than contradicting an existing rule, it does not require an ADR
amendment. The entity ISO code must appear in the detail slot header line adjacent to the
indicator and framework abbreviations, within the single-line height budget.

**Frontend Architect Agent:**
The `mda_alerts` API response returns one row per (mda_id, entity_id) pair — no backend-side
deduplication exists. Any UI-layer deduplication would require a custom aggregation transform
with no backend basis in `docs/schema/api_contracts.yml`. The population tiebreak (level 4 of
the ranking rule, §5.3) requires entity population metadata. Population is not currently a
field in the `mda_alerts` API response. The intent document must specify whether population
is injected into the alert payload at the backend, or resolved from a cached entity metadata
store accessible to the sort comparator without a new API call. Without this decision stated
as an observable application state specification, the level 4 sort cannot be implemented.

**PM Agent ruling — Q1: RESOLVED IN G7 with one additional mandatory intent document specification.**

No deduplication. Each entity-indicator-step triplet is a separate alert with its own display
row, own confidence tier, and own entity identity. The four-level ranking rule (§5.3) closes
the ADR-014 tiebreak gap. Entity identity (three-letter ISO 3166-1 alpha-3 code) appears in
the detail slot header and in every compact row entry.

*Additional mandatory specification from Frontend Architect:* The intent document must resolve
the entity population data availability question before implementation begins — whether population
figures are injected into the mda_alerts API payload, or resolved from a cached entity metadata
store without a new API call. If population data is unavailable in the current session context,
the level 4 tiebreak falls back to stable insertion-order sort. The chosen resolution must be
stated as an observable application state specification, not an implementation assumption.

---

#### Question 2: Causal grouping — cascading alerts from a shared parent event

*Context: The Hormuz shock chain: commodity price shock → reserve depletion (CRITICAL FIN) →
fiscal compression → HCL unemployment (WARNING HDI) → legitimacy fragility (WARNING GOV) →
programme survival risk (political economy module). All alerts share the originating Hormuz
event. Development Economist and Chief Methodologist question: what constitutes an independent
finding versus a cascade? Should Zone 1B group these under the originating event?*

**Design Thinking Agent:**
In the 90-second reactive window (Journey B Step 3), the analyst is in threat-identification
mode: "what is the most urgent breach I need to argue right now?" Causal grouping asks her
to simultaneously perform a second task: "what triggered these breaches, and which are effects
of the same cause?" These tasks are sequential — she identifies the threat first, then traces
its cause. A causal group header row in Zone 1B-compact interrupts the ranked-list scan
pattern and requires her to parse a parent-child hierarchy under time pressure — a
demonstrably slower cognitive operation. Zone 1B is the threat-identification surface; Zone 2
is the causal-analysis surface. Mode 3 causal attribution (already in ADR-014) handles the
one case where causation is deterministic and immediately relevant: she just applied a control
input and sees its direct consequence.

**Development Economist Agent:**
Each link in the Hormuz causal chain is analytically separable with distinct policy remediation
pathways: reserve depletion, HCL unemployment, and programme survival each require different
interventions and affect different cohorts. "Your conditionality package produced simultaneous
threshold breaches across financial and human development frameworks" IS a stronger negotiating
argument than treating them as coincidences — but constructing that argument requires first
establishing each breach's independent existence. The argument is built in preparatory mode
(before entering the room), not in the reactive window. In Zone 1B during a 90-second window,
the analyst needs the what before the why; Zone 2 is where the why is explored.

**Chief Methodologist Agent:**
The Hormuz causal chain traverses four distinct model relationships, each with its own
confidence tier: reserve depletion (Tier 2) → unemployment via Okun's law approximation
(Tier 3) → legitimacy fragility via synthetic political economy relationship (Tier 4) →
programme survival via M13 political economy module (Tier 4, direction-only). Each downstream
link degrades confidence — displaying "Caused by: Hormuz shock" across all four without
showing per-link confidence tiers implies the causal attribution is as certain as the
individual alerts, which it is not. In Mode 3, causal attribution is deterministic (the
analyst applied the control input) and is exempt from this constraint; in Mode 1/2 it is
inferred and cannot appear in Zone 1B without per-link disclosure.

**UX Designer Agent:**
A causal group header row in Zone 1B-compact is a new visual element with no basis in
ADR-014. Group headers consume compact sub-zone height, and any element that expands Zone
1B-compact's internal height budget touches the layout invariant — requiring an ADR amendment.
UX governing premise 2 ("instruments are always visible; context is navigable") places causal
context in Zone 2, the navigable surface. Mode 3 causal attribution (the single "Caused by:
[input]" line in Zone 1B-detail) is the correct Zone 1B causal surface: one line, within the
existing height budget, applied only where causation is deterministic.

**Frontend Architect Agent:**
Zone 1B causal grouping requires the `mda_alerts` API response to include a `parent_event_id`
or causal chain structure linking child alerts to their originating event. This field does not
exist in the current API contract (`docs/schema/api_contracts.yml`). The frontend has no basis
to infer parent event relationships from the current response shape — there is no client-side
workaround. Implementing causal grouping requires a backend schema change (new field on
mda_alerts), a corresponding migration, a new UI component (group header rows), new sort logic
that groups before ranking within groups, and possibly expand/collapse interaction state. This
is a multi-layer scope addition that falls entirely outside G7's implementation boundary.

**PM Agent ruling — Q2: EXPLICITLY DEFERRED.**

Mode 3 causal attribution for the top alert (the "Caused by: [input]" line in Zone 1B-detail,
ADR-014 §Mode 3 Auto-Update) remains in G7 scope, unchanged.

Full causal grouping in Zone 1B is out of G7 scope on five independent grounds: (1) requires
a backend schema field absent from the current API contract (Frontend Architect); (2) requires
a new Zone 1B layout element that touches the height invariant (UX Designer); (3) Mode 1/2
causal attribution carries per-link inference uncertainty not displayable in Zone 1B without
violating the confidence tier disclosure obligation (Chief Methodologist); (4) causal parsing
is the wrong cognitive task for the reactive entry state (Design Thinking); (5) each cascade
alert is an analytically independent finding that must retain its own display row (Development
Economist).

*Follow-on ADR required:* scope "Zone 1B causal grouping — propagation graph attribution for
Mode 1 and Mode 2, with per-link confidence tier disclosure, backend schema extension, and
Zone 2 navigation path." Number to be assigned from the ADR backlog at filing time.

---

#### Question 3: Alert storm handling — cognitive load ceiling for Zone 1B

*Context: 20+ simultaneous threshold breaches fire across frameworks, entities, and severity
levels. Is there a maximum count beyond which Zone 1B switches to a summary mode? At what
point does the instrument stop being kryptonite and start being noise? Design Thinking question:
what is the cognitive load ceiling for Zone 1B?*

**Design Thinking Agent:**
The cognitive load ceiling is the point at which Zone 1B shifts from providing useful scan
information to unusable scan information. Critically, ADR-014's architecture already handles
this: the analyst does not scan the compact list for the top finding — she reads it directly
from Zone 1B-detail (zero interactions, always visible). The compact list is an awareness
surface, not a search surface. In a 20-alert storm, she reads the detail slot (one fully
specified alert) and the compact list (2–4 visible rows, awareness scan) — effectively 3–5
data points, not 20. The "+N more ↕" converts the remainder to an awareness count ("there
are more") at no additional cognitive cost. No summary mode is needed; the current design
already handles alert storm conditions correctly without layout change.

**Development Economist Agent:**
An alert storm is multi-framework systemic collapse — the most severe scenario class in the
WorldSim model. In this condition, the analyst most needs to know which specific human
development thresholds have been crossed and which cohorts are affected. A summary mode
("20 ACTIVE alerts") is the least useful output in the most urgent scenario — it converts
specific evidence into an aggregate count that cannot be cited at the negotiating table. No
summary mode.

**Chief Methodologist Agent:**
A maximum count that truncates based on count rather than statistical significance is an
epistemic error: within same (severity, step_index), the higher-confidence alert (lower tier
number) is the stronger finding and should rank first regardless of volume. Adding
confidence_tier as a tertiary sort key (ascending — lower number = higher confidence) ensures
the most defensible finding occupies the highest rank under any alert volume. Summary modes
that aggregate alerts ("10 CRITICAL, 5 WARNING") produce a composite count with no defined
confidence tier — a statistical category that does not exist in this framework. No summary
mode. No maximum count.

**UX Designer Agent:**
No summary mode is consistent with the Zone 1B height invariant — any structure that changes
Zone 1B layout based on alert count requires an ADR amendment. The "+N more ↕" pattern must
appear whenever Zone 1B-compact overflows; N = total active alerts minus one (the top alert in
the detail slot). The confidence_tier tertiary sort is a ranking clarification within the
existing layout, not a new visual element — it is within G7 scope as an intent document
specification. An alert storm visual indicator (colored count pill in Zone 1B-compact header
when N ≥ threshold) is a new layout element requiring a follow-on ADR amendment; threshold
value is undefined.

**Frontend Architect Agent:**
Virtual scrolling is not needed at the alert volumes WorldSim produces — all mda_alerts rows
render in the DOM; CSS overflow clips Zone 1B-compact to its visible height. The "+N more ↕"
count is computed as (mda_alerts.length - 1) - visibleCompactRowCount, where
visibleCompactRowCount is derived from Zone 1B-compact's computed height divided by the fixed
row height (max 26px per row per UX Designer sign-off condition 1). The confidence_tier field
is already present in the mda_alerts API response — adding it as a tertiary sort key is a
one-line change to the sort comparator with no new API call required. No architectural changes
are needed for alert storm handling.

**PM Agent ruling — Q3: RESOLVED IN G7 with confidence_tier sort clarification; alert storm
visual indicator explicitly deferred.**

Resolved in G7 — must appear in intent document:
- No summary mode under any alert volume
- No maximum count truncation
- "+N more ↕" confirmed; N = (total_alerts - 1) - visible_compact_rows
- confidence_tier tertiary sort added to ranking rule (see §5.3); one-line comparator change

Explicitly deferred:
- Alert storm visual indicator (colored active-alert count pill in Zone 1B-compact header
  at threshold N) — new layout element; threshold undefined; requires follow-on ADR amendment

---

#### Question 4: Persistence versus new-alert distinction — consecutive breach count or separate alerts

*Context: A TERMINAL reserve_coverage_months alert (mda_id "X") fires at step 1 and remains
active through step 4. At step 5, consecutive_breach_steps increments to 5. Chief Methodologist
question: what constitutes a new finding versus continued evidence of the same finding? Does
this display as one persistent alert with an updating count, or as four separate alerts?*

**Design Thinking Agent:**
The analyst tracks "the reserve coverage crisis" as a single evolving situation, not as four
discrete events. A persisting TERMINAL is experienced as "the TERMINAL that started at step 1
and has not resolved" — not as "a TERMINAL at step 1, then another at step 2, then another at
step 3." Four separate alert rows for four steps of the same breach would fragment this singular
narrative and inflate the alert count, making the compact list harder to parse. The [NEW] badge
marks onset of a genuinely new finding (mda_id change); consecutive_breach_steps accumulates
the evidence of the persisting finding. Keep [NEW] narrow — applying it to count increments
would produce badge fatigue and cause analysts to miss genuine new-onset events.

**Development Economist Agent:**
The human cost argument gains force from duration. "This threshold has been breached for five
consecutive steps, accumulating human cost during each step of inaction" is a categorically
stronger argument than "a threshold was breached at step 1." The consecutive count is the
instrument's most important output for constructing a temporal argument at the negotiating
table. The count must update visibly between steps — a stale count at step 5 showing "4
consecutive steps" causes the analyst to cite weaker evidence than the data supports in a
live session. Human cost accumulates in real time; the instrument must reflect it in real time.

**Chief Methodologist Agent:**
A new finding is a new threshold crossing — a new (indicator, entity, threshold) triplet
crossing for the first time at a given step. Continued evidence is the same triplet remaining
crossed at subsequent steps. Consecutive steps are not independent observations of the same
event — they are temporally correlated samples from a single process. Treating them as four
separate findings is pseudo-replication. The `mda_id` is the natural primary key: one mda_id
per unique (indicator, entity, first_breach_step); all subsequent steps where the same
threshold remains breached update consecutive_breach_steps on the same mda_id. Confidence tier
does not change with consecutive count: the tier reflects the current step's data quality,
not the accumulated duration of the breach. An implementation that "upgrades" the label after
N consecutive steps is a statistical integrity violation.

**UX Designer Agent:**
This is already ADR-014's data model. One mda_id per finding; consecutive_breach_steps as the
persistence counter. [NEW] badge logic from ADR-014 §Mode 3 Auto-Update: badge appears when
and only when `mda_alerts[0].mda_id` changes between renders. Badge absent when same mda_id
persists and consecutive_breach_steps increments — that is an update to existing evidence.
ADR-014 §Silent Failure 4 specifies the observable application state test; §Silent Failure 2
specifies the consecutive count liveness test. Both must be referenced in the G7 intent
document and included in the QA test file.

**Frontend Architect Agent:**
The backend already implements the one-alert-per-mda_id model: `mda_alerts` returns one row
per mda_id with stable identity across steps and consecutive_breach_steps updating on each
advance. Frontend rendering re-sorts and re-renders the full mda_alerts list on each step
advance — no "persistent alert" state tracking is needed in the frontend. The stale memoisation
risk is specific: React useMemo or useCallback hooks that compare mda_alerts by array reference
rather than content will hold stale consecutive_breach_steps values if the Redux store returns
the same array reference across step advances. The intent document must specify that mda_alerts
sort and render invalidate on every step advance, not memoised on alert list reference equality.
This is observable: a step advance where no new alerts are added or removed must still trigger
re-render with the updated consecutive_breach_steps value.

**PM Agent ruling — Q4: RESOLVED IN G7 with three mandatory intent document specifications;
deepening signal noted as a future design issue (no ADR required).**

1. **[NEW] badge logic:** Badge appears when and only when `mda_alerts[0].mda_id` changes
   between renders. Badge absent when same mda_id persists and consecutive_breach_steps
   increments. Observable application state: ADR-014 §Silent Failure 4 test required in QA file.

2. **Consecutive count liveness and memoisation boundary:** `consecutive_breach_steps` renders
   from live API state on each step advance. mda_alerts sort and render must invalidate on every
   step advance — not memoised on alert list reference equality. Observable: a step advance with
   no new/removed alerts must still re-render Zone 1B-detail with updated consecutive_breach_steps.
   ADR-014 §Silent Failure 2 test required in QA file.

3. **Confidence tier is per-step, not cumulative:** `getNegotiationLabel(confidence_tier)` renders
   the current step's confidence_tier. Label does not change as a function of consecutive count.
   Observable: advance four steps with same TERMINAL alert persisting; assert confidence label
   text is identical at step 1 and step 4.

Noted as future design issue (no ADR required):
- Visual styling distinction when consecutive count ≥ threshold (e.g., bold at ≥3 steps) — a
  component styling decision; file as a follow-on design issue when visual treatment is defined.

---

#### Question 5: Alert lifecycle management — dismiss and archive

*Context: No dismiss or archive capability currently exists in Zone 1B. Should the analyst be
able to mark an alert as acknowledged — visually distinguishing alerts she has already cited
from new alerts she has not yet processed? Design Thinking question: at what point does a read
alert become noise rather than evidence?*

**Design Thinking Agent:**
The question is whether Zone 1B should be a passive monitoring surface (always reflects current
model state) or a managed notification surface (allows analyst annotation of model state). In a
negotiation room, the persistent presence of the TERMINAL reserve alert — still in the detail
slot — serves a purpose: it confirms the finding has not resolved. A dismissed alert that
continues to deepen creates an active monitoring gap. More fundamentally: dismiss/archive requires
the analyst to take a deliberate action in Zone 1B, adding interaction to a zero-interaction
instrument. The [NEW] badge already handles the "something new arrived" signal without requiring
dismissal of the old signal. If the analyst needs to track what she has argued, that is a session
annotation capability belonging in Zone 2 or a future session management layer — not Zone 1B.
The line is clear: Zone 1B reflects model state; analyst annotations are a separate concern.

**Development Economist Agent:**
A dismissed alert that remains active in the model represents a humanitarian crisis the analyst
has chosen to stop watching. In a live negotiation, reserve coverage does not stop declining
because she acknowledged the alert — the consecutive count keeps incrementing. Dismiss creates
a risk that she loses track of a worsening situation precisely because she thought she had
handled it. The human cost ledger must not be suppressible by analyst annotation state. Any
acknowledge capability must not visually diminish or remove active threshold breaches from view.

**Chief Methodologist Agent:**
A "dismissed" alert that continues to be breached creates a divergence between display state
(dismissed) and analytical state (still breached, still accumulating consecutive steps). This
is a shadow gap: the visual representation no longer accurately reflects simulation reality.
The tool's integrity depends on its display matching model state. If the analyst dismisses the
TERMINAL reserve alert at step 3 and it reaches 7 consecutive steps at step 9 but the display
shows "acknowledged," she is operating on a materially outdated picture of the analytical
situation. No annotation mechanism may suppress or visually diminish an active threshold breach.

**UX Designer Agent:**
A dismiss button or acknowledge action in Zone 1B adds interaction to a zero-interaction
instrument — a direct contradiction of UX governing premise 2. This is not a minor addition:
it changes Zone 1B's interaction model from read-only evidence surface to managed notification
surface. The visual design for an acknowledged state (muted styling? checkmark? strikethrough?)
requires a new visual vocabulary with no basis in ADR-014. Implementing dismiss/archive in Zone
1B requires a separate ADR that explicitly addresses the governing premise conflict, defines the
acknowledged state's visual treatment, and specifies the interaction pattern. The preferred path,
if this capability is desired, is a Zone 2 annotation surface that preserves Zone 1B's
zero-interaction contract.

**Frontend Architect Agent:**
Dismiss/archive requires: (1) a new `acknowledged: boolean` or `dismissedAt: timestamp` field
in the frontend alert store per mda_id; (2) filter or visual-state logic in Zone 1B-detail and
Zone 1B-compact; (3) an archive surface to view dismissed alerts (Zone 2 or separate panel —
unspecified); (4) a persistence decision: session-only (React state, resets on reload) or
backend-persisted (requires a new PATCH /scenarios/{id}/alerts/{mda_id}/ack endpoint and
corresponding schema change). The session-only variant alone requires a new state management
concern and a new Zone 1B interaction model. The backend-persisted variant adds a new API
endpoint and migration entirely outside G7's scope. Neither variant is implementable within
G7's implementation boundary.

**PM Agent ruling — Q5: EXPLICITLY DEFERRED.**

Dismiss/archive in Zone 1B is out of G7 scope on five independent grounds: (1) adds interaction
to a zero-interaction instrument (UX governing premise 2 violation — ADR required); (2) creates
a shadow gap between display state and model state (Chief Methodologist constraint — non-
negotiable integrity requirement); (3) creates monitoring risk for deepening alerts in live
sessions (Development Economist constraint); (4) requires a new visual vocabulary not specified
in ADR-014; (5) requires either a new backend API endpoint (persisted) or a new frontend state
management concern (session-only) — both outside G7's scope.

*Follow-on ADR required:* scope "Alert lifecycle management — acknowledge and archive in Zone
1B or Zone 2, with display-vs-model-state integrity constraints and persistence model." The ADR
must explicitly address the UX governing premise 2 conflict and the Chief Methodologist
constraint that active threshold breaches must not be suppressible by analyst annotation. The
Development Economist and Chief Methodologist constraints are non-negotiable inputs to that ADR.

---

#### Question 6: Alert-to-graph visual linking — Zone 1A/Zone 1B bidirectional coupling

*Context: Zone 1A (trajectory chart) shows framework composite scores; Zone 1B alerts name
specific indicators. Selecting or hovering an alert in Zone 1B could highlight the corresponding
step or indicator on Zone 1A. This capability is specified in user-stories-public-advocacy-m10.md
and PI-REVIEW-002 as desired bidirectional Zone 1 coupling but is not implemented. Is it in G7
scope or deferred?*

**Design Thinking Agent:**
Alert-to-graph linking is a "point of interest" interaction: the analyst selects an alert, the
trajectory chart highlights the step where the breach occurred, and she sees the trajectory that
led to it. This is analytically powerful — it shows HOW reserves arrived at the breach point,
not just that they breached. However, this is a preparatory-state capability (Journey D: she
is constructing her argument before entering the room), not a reactive-state capability (Journey
B: she is reading evidence during negotiation). Zone 1B is designed for the reactive window.
Adding hover/click to Zone 1B for trajectory coupling adds interaction to a zero-interaction
surface — the same design constraint that blocks dismiss/archive. The preferred path: an
alert-triggered navigation to Zone 2 (clicking an alert opens the FrameworkPanel for the
relevant framework, pre-scrolled to the alert step) satisfies the visual linking intent without
touching Zone 1B's interaction model.

**Development Economist Agent:**
The trajectory context behind a threshold breach matters for argument construction: "this
threshold has been approached slowly over eight steps" is a different analytical claim from
"this threshold was crossed in a single spike." The trajectory curve shows which is true. But
the analyst constructs this argument in preparatory mode — before entering the negotiating room.
The Zone 2 navigation path (alert-triggered FrameworkPanel navigation) would satisfy this need
without touching Zone 1B. The Zone 1A/1B bidirectional coupling is a meaningful capability
that should be prioritized after G7 stabilises the Zone 1B layout.

**Chief Methodologist Agent:**
Zone 1A displays framework composite scores; Zone 1B alerts name specific indicators. The
mapping from indicator to framework composite is deterministic: FIN alerts map to the Financial
composite; HDI to Human Development; ECO to Ecological; GOV to Governance. This mapping is
available in the `framework` field of the `mda_alerts` response — the data dependency for
alert-to-graph linking already exists in the current API. The question is implementation scope
and interaction model, not data availability.

**UX Designer Agent:**
Zone 1B is a zero-interaction instrument. Adding hover or click to Zone 1B-detail or Zone
1B-compact for trajectory highlighting adds interaction to a zero-interaction surface — the
same UX governing premise 2 boundary that blocks dismiss/archive. A Zone 2 navigation
alternative (clicking an alert navigates to the relevant FrameworkPanel) adds one interaction
to Zone 1B but is narrower than a hover-based persistent coupling. Whether that single
navigation click is acceptable in Zone 1B requires a governing premise ruling in a new ADR
— it is less invasive than dismiss/archive, but still adds interaction. The existing
specification references (`user-stories-public-advocacy-m10.md`, `PI-REVIEW-002`) are
authority documents for the follow-on ADR's persona trace. G7 must not add any hover or
click handler to Zone 1B rows — any such handler discovered during implementation must be
extracted to a separate PR.

**Frontend Architect Agent:**
Alert-to-graph highlighting requires shared state between Zone 1A (TrajectoryView) and Zone
1B (MDAAlertPanelZone1B) that does not currently exist. These are sibling components within
InstrumentCluster.tsx with no direct prop channel. Coupling them requires either: (1) lifting
"highlighted alert" state to InstrumentCluster.tsx and passing it down to both siblings as
props — adding a new state concern to a currently layout-only component; or (2) a new Redux
store slice for Zone 1 coupling state. The Zone 1A chart (Recharts) would need a new prop to
accept a highlighted step or framework and render a reference line or custom cursor accordingly.
Scope estimate: 200–400 lines across InstrumentCluster.tsx, TrajectoryView.tsx, and the
Recharts chart configuration. This is a distinct architectural concern from the Zone 1B layout
rewrite and should be a separate implementation group with its own intent document.

**PM Agent ruling — Q6: EXPLICITLY DEFERRED.**

Alert-to-graph Zone 1A/1B bidirectional coupling is out of G7 scope on three independent
grounds: (1) Zone 1B hover/click interaction contradicts UX governing premise 2 — requires its
own ADR to resolve, including assessment of the Zone 2 navigation alternative; (2) Zone 1A/1B
shared state is a new architectural concern distinct from the Zone 1B layout rewrite, estimated
at 200–400 lines across three components (Frontend Architect); (3) the Zone 2 navigation path
(preferred by UX Designer) is an untested design path that requires deliberation before
implementation.

*Follow-on ADR required:* scope "Zone 1A/1B bidirectional coupling — alert-triggered trajectory
highlight, Zone 2 navigation path, and UX governing premise 2 resolution." Existing authority
documents for persona trace: `user-stories-public-advocacy-m10.md`, `PI-REVIEW-002`.

G7 must not add any hover or click handler to Zone 1B-detail or Zone 1B-compact rows. Any Zone
1A/1B coupling behavior encountered during implementation must be extracted to a separate PR
targeting a future sprint group.

---

### 5.2 — PM Agent Ruling Summary

| Question | Ruling | Status |
|---|---|---|
| Q1 — Deduplication (same-indicator multi-entity) | No deduplication; four-level ranking rule; entity ISO code in both surfaces; population data availability resolved in intent document | **Resolved in G7** |
| Q2 — Causal grouping (cascading alerts, Hormuz chain) | Mode 3 causal attribution unchanged; Zone 1B causal grouping out of scope (backend schema gap + height invariant + per-link confidence disclosure + cognitive task mismatch) | **Explicitly deferred** — follow-on ADR required |
| Q3 — Alert storm handling | No summary mode, no count cap; "+N more ↕" confirmed; confidence_tier tertiary sort added; alert storm visual indicator deferred | **Resolved in G7** (visual indicator deferred) |
| Q4 — Persistence vs. new-alert | One alert per mda_id; consecutive count liveness and memoisation boundary; [NEW] = mda_id change; confidence tier per-step | **Resolved in G7** — three intent document specifications required |
| Q5 — Dismiss and archive | Out of scope: zero-interaction violation + shadow gap + monitoring risk + no visual vocabulary + backend/state scope | **Explicitly deferred** — follow-on ADR required |
| Q6 — Alert-to-graph visual linking | Out of scope: Zone 1B hover/click contradicts governing premise 2; Zone 1A/1B shared state is a separate architectural concern; Zone 2 navigation path untested | **Explicitly deferred** — follow-on ADR required |

---

### 5.3 — Full Ranking Rule (closes Q1 and Q3 gaps in ADR-014)

ADR-014 §Top-Alert Ranking Rule specifies two sort levels. This section adds two further
tiebreak levels covering the multi-entity and high-confidence-tie cases not present in the
original single-entity design context. The extension fills unspecified cases — it does not
contradict existing rules. Authority: Section 5 panel deliberation, 2026-06-12 (amended).
An ADR amendment may be filed if EL directs at review.

**Four-level ranking rule (complete):**

| Level | Sort key | Direction | Rationale |
|---|---|---|---|
| 1 | `severity` | DESC — TERMINAL (0), CRITICAL (1), WARNING (2) | Most urgent finding first |
| 2 | `step_index` | ASC — earliest breach first | Longest consecutive count → strongest argument evidence |
| 3 | `confidence_tier` | ASC — lower number = higher confidence ranks first | Most defensible finding wins within same (severity, step_index) |
| 4 | Entity population size | DESC — larger affected population ranks first | Human cost ledger priority; deterministic and semantically motivated |

Stable insertion-order sort for any alerts that tie on all four levels.

Detail slot shows the alert ranked first. Compact list shows all remaining alerts in the same order.

**Implementation note (Frontend Architect):** Level 4 requires entity population metadata. The
intent document must specify whether population is available in the mda_alerts API response or
resolved from a cached entity metadata store. Level 4 falls back to stable insertion-order sort
if population data is unavailable.

---

### 5.4 — Mandatory Intent Document Specifications from Resolved Questions

The following specifications must appear in the G7 intent document in addition to the three UX
Designer conditional sign-off requirements (Section 2.3). Together these constitute the complete
pre-implementation specification set for G7.

**From Q1 (deduplication / ranking rule):**
- No deduplication at any level; four-level ranking rule from §5.3
- Entity identity (three-letter ISO 3166-1 alpha-3 code) in detail slot header and every compact row
- Entity population data availability resolution (backend injection or cached metadata store)

**From Q3 (alert storm):**
- No summary mode under any alert volume
- No maximum count truncation
- "+N more ↕" present whenever compact list overflows; N = (total_alerts - 1) - visible_compact_rows
- confidence_tier tertiary sort in ranking rule (one-line comparator change)

**From Q4 (persistence / new-alert):**
- [NEW] badge appears on mda_id change only; absent on consecutive count increment (ADR-014 §Silent Failure 4 test required in QA file)
- mda_alerts sort and render invalidate on every step advance — not memoised on alert list reference equality (ADR-014 §Silent Failure 2 test required in QA file)
- Confidence tier label is per-step, not cumulative (observable: label identical at step 1 and step 4 for same persisting alert)

---

### 5.5 — Deferred Items and Follow-on ADR References

| Item | Grounds for deferral | Follow-on action |
|---|---|---|
| Zone 1B causal grouping — Mode 1/2 propagation attribution | Backend schema gap; height invariant violation; per-link confidence disclosure obligation; cognitive task mismatch for reactive window | Follow-on ADR: "Zone 1B causal grouping — Mode 1/2 propagation graph attribution with per-link confidence tier disclosure, backend schema extension, and Zone 2 navigation path" |
| Alert storm visual indicator — active-alert count pill in Zone 1B-compact header | New layout element; threshold value undefined; ADR-014 amendment required | Follow-on ADR amendment to ADR-014 when threshold and visual treatment are defined |
| Deepening signal — styling change when consecutive count ≥ threshold | Pure component styling decision; no architectural change; badge vocabulary must remain narrow | Follow-on design issue (not ADR) when visual treatment is defined |
| Alert lifecycle management — dismiss and archive | Zero-interaction violation; shadow gap between display and model state; monitoring risk; requires new visual vocabulary and new backend or frontend state scope | Follow-on ADR: "Alert lifecycle management — acknowledge and archive in Zone 1B or Zone 2, with display-vs-model-state integrity constraints and persistence model" |
| Alert-to-graph visual linking — Zone 1A/1B bidirectional coupling | Zone 1B hover/click contradicts UX governing premise 2; Zone 1A/1B shared state is a distinct architectural concern; Zone 2 navigation path untested | Follow-on ADR: "Zone 1A/1B bidirectional coupling — alert-triggered trajectory highlight, Zone 2 navigation path, and UX governing premise 2 resolution." Authority documents: `user-stories-public-advocacy-m10.md`, `PI-REVIEW-002` |

---

## Section 6 — Near-Miss Sweep

**Near-miss sweep date:** 2026-06-12
**Sweep period:** Since M13 Sprint 1 entry filed (2026-06-12, same session)

| Finding | Category | PI Agent register call issued? | NM entry number |
|---|---|---|---|
| None — G7 was correctly listed as BLOCKED_ADR in Sprint 1 entry; ADR-014 authored and accepted in same session; no process gap identified in the G7 unblock sequence | N/A | N/A | N/A |

*Note on NM-042 and UX Designer sign-off:* NM-042 (structured sign-off attestation, PR #930)
amended the UX Designer sign-off protocol to require four named fields: Reviewing agent, Session
context, Governing documents reviewed (named sections), and Concerns found. ADR-014's sign-off
block was authored in the pre-NM-042 format and was updated to the four-field structured
attestation form as a housekeeping step at sprint entry filing (2026-06-12), before any
implementation PR was opened. The updated sign-off reads: `Same session as ADR authorship —
acknowledged`; seven governing document sections named; three concerns on record. EL is required
to verify the governing document citations (named sections, not generic references) at ADR
acceptance, per CLAUDE.md §UX Designer sign-off. No further near-miss action required for G7
from NM-042.

---

## EL Approval Record

**EL approval:** 2026-06-13

> G7 sprint entry approved. Section 5 six-question deliberation on record. Resolved specifications (Q1, Q3, Q4) must appear in the intent document before implementation PR opens. Q2, Q5, Q6 explicitly deferred with follow-on ADR scope on record. Implementation may proceed once intent document and QA test file are filed per Phase A lifecycle (Section 2.3 and 2.4 gates).
> — @PublicEnemage (2026-06-13)
