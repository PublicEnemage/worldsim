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
*(Authority: CLAUDE.md §Agent Execution Lifecycle Step 1)*

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

**Section 5 additional intent document requirements:** The alert collision and decluttering
panel deliberation (Section 5 below) resolves four additional specifications that must appear
in the intent document alongside the three UX Designer conditions above. See §5.2 PM Agent
Ruling Summary for the complete list.

### 2.4 — QA test authorship gate

*QA tests must be authored from the intent document's acceptance criteria before implementation
code is written.*
*(Authority: CLAUDE.md §Agent Execution Lifecycle Step 2)*

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

## Section 5 — Alert Collision and Decluttering Scope Declaration

*Panel deliberation: 2026-06-12. Panel: Development Economist Agent, Chief Methodologist Agent,
Design Thinking Agent, UX Designer Agent. PM Agent synthesises into rulings.*

*Purpose: ADR-014 specifies the Zone 1B layout model but does not specify behaviour for
four alert display edge cases that will arise during implementation. Resolving them now — before
the intent document is authored — prevents scope negotiation at Step 3 (implementation). Each
ruling is either "resolved in G7 with stated specification" or "explicitly deferred with rationale
and follow-on ADR reference."*

*EL endorsement of these rulings is required alongside sprint entry approval. A ruling marked
"resolved in G7" that is subsequently challenged mid-implementation returns to this panel —
it does not unilaterally narrow.*

---

### 5.1 — Panel Deliberation

---

#### Question 1: Deduplication rule for same-indicator multi-entity alerts at the same step

*Context: In a multi-entity scenario (JOR + EGY), both entities may breach the same indicator
at the same step — e.g., reserve_coverage_months TERMINAL at step 3 for both. Both appear
as distinct rows in `mda_alerts`. ADR-014's ranking rule specifies (severity DESC, step_index
ASC) but does not name a tiebreak when two alerts share both severity and step_index.*

**Development Economist Agent:**
Jordan's 5.1 million population and Egypt's 104 million are not interchangeable data points.
Collapsing a dual-entity TERMINAL breach into a single deduplicated row suppresses the
magnitude asymmetry — the human cost case for Egypt is approximately twenty times larger.
The finance minister's analyst needs both to be visible because the negotiating argument has
two tracks: severity of the breach and scale of the population bearing the cost. If forced to
choose one for the detail slot, the larger-population entity's alert is the stronger argument
at a negotiating table — it names more people. Do not deduplicate. The detail slot shows the
higher-population alert; the other falls to the compact list's first row.

**Chief Methodologist Agent:**
Jordan's reserve_coverage_months and Egypt's reserve_coverage_months are independent
statistical observations. They have separate confidence tiers, separate data provenance (one
may be Tier 2 observed; the other Tier 3 synthetic), and potentially different methodology
for gap-filling. A deduplicated "JOR + EGY" alert would imply a composite statistical basis
that does not exist and would require a composite confidence tier that is not defined by any
method in the framework. Deduplication is a statistical integrity violation. Each
entity-indicator-step triplet is a distinct observation and must be displayed as such. Within
a tiebreak between two alerts sharing (severity, step_index), the higher-confidence alert
(lower tier number) is the stronger evidentiary claim and ranks first — that is the Chief
Methodologist's primary tiebreak; entity population is a secondary tiebreak for cases where
confidence tier is also equal.

**Design Thinking Agent:**
The analyst's mental model is entity-contextualised throughout. She tracks Jordan and Egypt
as two separate national situations, not as a regional aggregate. A merged "JOR + EGY" row
maps to no single country in her cognitive frame and breaks the thread she is maintaining.
The deduplication impulse typically comes from visual-clutter concern — but the compact list
already handles clutter through the "+N more ↕" overflow pattern. The correct solution to
visual crowding is the compact list, not deduplication. The tiebreak question (which entity
gets the detail slot) must be deterministic and semantically motivated — not alphabetical,
not insertion-order. Entity population satisfies that requirement because it aligns with the
human cost priority that governs the rest of the instrument.

**UX Designer Agent:**
No deduplication is consistent with UX-1: Zone assignment requires entity identity as part
of each alert's key. The entity name (three-letter ISO code) appears in the detail slot header
and in each compact row — removing it through deduplication would strip a required field.
The multi-entity tiebreak is an unspecified case in ADR-014 §Top-Alert Ranking Rule, which
was written for single-entity scenarios. The gap must be closed in the G7 intent document as
an extension of the ranking rule. Because the extension fills an unspecified case rather than
contradicting an existing rule, it does not require an ADR amendment — the intent document
is the authority. The entity ISO code must appear in the detail slot header line adjacent to
the indicator and framework abbreviations, within the single-line budget.

**PM Agent ruling — Q1: RESOLVED IN G7.**

No deduplication at any level. Each entity-indicator-step triplet is a separate alert with its
own display row. The ranking rule is extended with two additional tiebreak levels to cover
the multi-entity case (see §5.3 for the full four-level rule). Entity identity (three-letter
ISO 3166-1 alpha-3 code) must appear in the detail slot header and in every compact row entry.
This specification must appear in the G7 intent document. It is within ADR-014's scope.

---

#### Question 2: Causal grouping for cascading alerts sharing a parent event

*Context: A commodity price shock at step 2 causes reserve drawdown (CRITICAL FIN) AND public
sector wage compression (WARNING HDI for healthcare cohort). Both alerts share the same parent
event. Should Zone 1B surface the shared causation — e.g., by visually grouping the two alerts
under a "Caused by: [event]" header in the compact list?*

**Development Economist Agent:**
Causal grouping is analytically important: "your conditionality package produced simultaneous
threshold breaches across financial and human development frameworks" is a categorically
stronger negotiating argument than "two separate threshold breaches happened to coincide."
The shared parent makes the IMF's proposed timeline responsible for the compound effect, not
just the individual breach. However, this argument requires the analyst to be in a
root-cause reasoning mode — she needs to understand why, not just what. In a 90-second
reactive window, she is establishing the what first. Causal grouping in Zone 1B would push
her into the why before she has finished reading the what. The correct instrument for the
causal argument is Zone 2, where she navigates when she has the situational awareness
established. Mode 3 causal attribution (already in ADR-014) handles the one case where
causation is unambiguous and immediately relevant: she just applied a control input and
wants to see its direct consequence.

**Chief Methodologist Agent:**
In Mode 3 (control inputs are explicit), causal attribution is deterministic — the propagation
graph was invoked with a specific root event and the downstream threshold crossings are direct
model outputs. In Mode 1 (historical replay) and Mode 2 (projected simulation), causal
attribution requires inferring root causes from the propagation graph — an inference that
carries its own confidence tier. The causal link between a parent event and a downstream
threshold breach may be Tier 3 or Tier 4, independent of the breach alert's own tier.
Displaying a causal group label in Zone 1B for Mode 1/2 without displaying the causal link's
confidence tier is a disclosure violation equivalent to omitting the alert's own tier.
The causal inference belongs in Zone 2 where the full propagation view can show confidence
per link. Mode 3 causal attribution in the detail slot is exempt because the attribution is
deterministic, not inferred.

**Design Thinking Agent:**
A causal group header row in Zone 1B-compact ("Alerts caused by: EmergencyPolicyInput Step 2")
adds a parsing task that is categorically different from reading a ranked severity list. In
threat-assessment mode, the analyst reads left-to-right and top-to-bottom for the most urgent
signal. A grouping structure interrupts this scan pattern and asks her to first understand
the parent-child relationship, then locate the specific alerts within it. This is a higher-order
cognitive task that adds to the interaction budget without increasing her immediate situational
awareness. The instrument is most useful in the reactive window when its reading pattern is
maximally simple. The causal argument — which IS a genuine analytical value — is the Mode 2
zone where she goes once she knows what happened and needs to understand why.

**UX Designer Agent:**
A causal group header row in Zone 1B-compact is a new visual element with no basis in ADR-014.
Adding it would require layout modifications that could affect Zone 1B height: group headers
consume vertical space, and the compact sub-zone already has a fixed height contract. Any new
element that could affect Zone 1B-compact's internal height budget requires an ADR amendment
because it touches the layout invariant. UX governing premise 2 ("instruments are always visible;
context is navigable") establishes the principle directly: causal context is navigable content —
it belongs in Zone 2 (FrameworkPanel propagation view), which the analyst opens when she is in
preparatory mode. Mode 3 causal attribution (the single "Caused by: [input]" line) is the
correct Zone 1B causal surface: it is one line, within the existing height budget, and applies
only where causation is deterministic.

**PM Agent ruling — Q2: EXPLICITLY DEFERRED.**

Mode 3 causal attribution for the top alert (the single "Caused by: [input]" line in Zone
1B-detail) remains in G7 scope, unchanged from ADR-014 §Mode 3 Auto-Update. No change.

Full causal grouping — visual grouping of multiple alerts by shared parent event in Zone
1B-compact — is explicitly out of G7 scope. Grounds: (1) requires a new layout element
that touches the Zone 1B height invariant (ADR amendment required); (2) Mode 1/2 causal
attribution carries an inference confidence tier that cannot be displayed in Zone 1B without
a new field (Chief Methodologist constraint); (3) adds a parsing structure inappropriate for
the reactive entry state (Design Thinking constraint); (4) zone principle assigns causal
context to Zone 2 (UX constraint).

*Follow-on ADR required:* scope "Zone 1B causal grouping — propagation graph attribution for
Mode 1 and Mode 2 with per-link confidence tier disclosure." Number to be assigned from the
ADR backlog at the time of filing.

---

#### Question 3: Alert storm handling — maximum alert count or summary mode

*Context: 20+ simultaneous threshold breaches fire across frameworks, entities, and severity
levels. What is Zone 1B's display contract under extreme alert volume? Is there a maximum
count beyond which the compact list switches to a summary mode, or does the "+N more ↕"
pattern extend without limit?*

**Development Economist Agent:**
An alert storm — 20+ simultaneous breaches — is itself an analytically significant event: it
signals multi-framework systemic collapse, the most serious scenario class the tool models.
Suppressing individual alerts behind an aggregate count ("20 ACTIVE") is precisely the wrong
response to the most mission-critical scenario. The analyst needs to know which specific human
development thresholds have been crossed and which cohorts are affected — not that some large
number of things have gone wrong. The detail slot must continue to show the top alert in full.
The compact list must continue to show the ranked list of remaining alerts, scrollable. The
"+N more ↕" pattern is correct — it signals that more exist without changing the layout or
hiding the ranked structure. No summary mode under any volume.

**Chief Methodologist Agent:**
A maximum count that truncates the compact list would suppress findings ranked by count rather
than statistical significance. The correct priority axis is the ranking rule — severity,
then step_index, then confidence. An alert ranked 15th in a 20-alert storm may have a higher
confidence tier than an alert ranked 4th; truncating at 10 would suppress a statistically
stronger finding in favour of a weaker one. Summary modes that replace the ranked list with
aggregate counts (e.g., "10 CRITICAL, 5 WARNING") collapse confidence tiers into a single
aggregate, which does not exist as a defined statistical quantity. Within same (severity,
step_index), the higher-confidence alert (lower tier number) ranks first — this should be
added as a tertiary sort key to the ranking rule, so the most defensible finding occupies
the highest visible rank under pressure. No maximum count. No summary mode.

**Design Thinking Agent:**
The "+N more ↕" pattern in ADR-014 Scenario C (10 alerts) is the correct and sufficient
mechanism for high-volume alert scenarios. It communicates that more alerts exist without
changing the layout, breaking the ranked-list pattern, or requiring the analyst to adopt a
new reading strategy. A summary mode would change the instrument's interface under exactly
the conditions when interface stability is most valuable. The Zone 1B-compact scroll is the
designed release valve for volume — analysts who need to see all alerts can scroll; the most
urgent is always in the detail slot. A secondary visual signal when the count passes a
threshold (e.g., a colored active-count pill at ≥10) is worth noting as a future design
consideration, but it is not a G7 scope item: it adds a new visual element that requires
design specification.

**UX Designer Agent:**
No summary mode is consistent with the Zone 1B height invariant — any mode that changes
the layout structure of Zone 1B based on alert count would require an ADR amendment. The
"+N more ↕" pattern must be present whenever the compact list overflows Zone 1B-compact's
visible height. The count (N) must be accurate: it is the total count of active alerts minus
one (the top alert in the detail slot). The Chief Methodologist's confidence_tier tertiary sort
key is a ranking clarification, not a layout change — it is within G7 scope as an intent
document specification, closing the ADR-014 gap that only specifies two tiebreak levels. An
alert storm visual indicator (colored count pill in Zone 1B-compact header when N ≥ threshold)
is a new layout element and requires a follow-on design specification and ADR amendment.

**PM Agent ruling — Q3: PARTIALLY RESOLVED IN G7; alert storm visual indicator explicitly deferred.**

Resolved in G7 — must appear in the intent document:
- No summary mode under any alert volume: confirmed within ADR-014 scope
- No maximum count truncation: confirmed within ADR-014 scope
- "+N more ↕" indicator: confirmed; must appear whenever compact list overflows; N equals
  total active alert count minus one
- Confidence_tier tertiary sort (see §5.3): resolved in G7 as a ranking rule clarification

Explicitly deferred:
- Alert storm visual indicator (e.g., colored active-alert count pill in Zone 1B-compact
  header when active count ≥ N) — adds a new visual element; requires follow-on design
  specification and ADR amendment. Threshold value (N) is undefined. Out of G7 scope.

---

#### Question 4: Persistence vs. new-alert distinction for multi-step breaches

*Context: A TERMINAL reserve_coverage_months alert (mda_id = "X") has been active for four
consecutive steps. At step 5, consecutive_breach_steps increments to 5. How does Zone 1B
signal that this alert is deepening (persistent, worsening) vs. that a new alert just fired?
When should [NEW] appear, and when should it not?*

**Development Economist Agent:**
Consecutive breach count is the primary persistence evidence and the most important number in
the detail slot for negotiating argument construction. "This threshold has been breached for
five consecutive steps" establishes a trajectory that predates the current negotiation session —
the damage has been compounding before the analyst entered the room. The count must update
visibly between steps: if the analyst reads "4 consecutive steps" at step 4 and then "5
consecutive steps" at step 5, she observes the accumulation directly. The critical failure
mode is stale count: if memoisation holds the count at 4 while the scenario is at step 5,
the analyst cites wrong evidence in a live session. Persistence and new-alert are not the
same thing — the [NEW] badge is right for the latter; the count update is right for the
former.

**Chief Methodologist Agent:**
Consecutive breach count accumulates events but does not accumulate statistical confidence.
A 5-step TERMINAL breach based on Tier 3 data at each step is not more certain than a 1-step
breach — it is more persistent. The confidence label ("Moderate confidence — cite with caveat")
is a property of the current step's underlying data tier, not a function of how many times
the threshold has been crossed. An implementation that "upgrades" the confidence label after
N consecutive steps would be a statistical integrity violation. The label must render from
the current step's confidence_tier for the top-ranked alert — not from a cumulative function
of past steps. This must be stated explicitly in the intent document because it is
counter-intuitive: analysts may expect that repeated confirmation increases certainty. The
tool must not reinforce that misreading.

**Design Thinking Agent:**
The [NEW] badge is a precise signal: "something replaced the previous top alert." The analyst
parses it as "I need to look again — the situation changed." Applying [NEW] to a persisting
alert that merely incremented its consecutive count would overload this signal — the analyst
would be prompted to re-examine evidence she already knows. Badge fatigue follows: if [NEW]
appears constantly on deepening alerts, the analyst stops attending to it, and misses genuine
new-onset events. Keep [NEW] narrow — mda_id change only. For the "deepening" case
(consecutive count increment on the same alert), the passive text update is the correct and
sufficient signal. A visual styling distinction when consecutive count reaches a threshold
(e.g., bold text or color change at ≥3 steps) is worth noting as a future design detail —
it would make the "long-running breach" state more visually distinct without introducing a
new badge type. That decision belongs in the intent document as a design detail, not a
separate ADR.

**UX Designer Agent:**
[NEW] badge logic from ADR-014 §Mode 3 Auto-Update: the badge appears when and only when
`mda_alerts[0].mda_id` changes between renders — a genuinely different alert has displaced
the previous top. The badge does NOT appear when the same `mda_id` persists and only
`consecutive_breach_steps` increments. This distinction is already correct in ADR-014 and
must be preserved exactly in the intent document. The implementation risk (Silent Failure 4
in ADR-014) is that the change-detection logic uses referential equality on the alerts array
rather than `mda_id` string comparison, which would fail to set [NEW] when it should.
The intent document's observable application state for [NEW] is already specified in ADR-014
§Silent Failure 4; the G7 intent document must reference it explicitly. Consecutive count
liveness is Silent Failure 2 in ADR-014 — also already specified; must be referenced. A
"deepening" badge is future scope and, unlike the alert storm visual indicator, does not
require a separate ADR — it is a styling decision within the existing Zone 1B-detail component
that can be handled as a follow-on design issue.

**PM Agent ruling — Q4: RESOLVED IN G7 with three intent document specifications; deepening
signal noted as a future design issue.**

Resolved in G7 — all three must appear explicitly in the G7 intent document:

1. **[NEW] badge logic — mda_id comparison, not step-index comparison:**
   [NEW] badge appears when and only when `mda_alerts[0].mda_id` changes between renders.
   Badge does NOT appear when the same `mda_id` persists and `consecutive_breach_steps`
   increments. Observable application state (from ADR-014 §Silent Failure 4): in a Mode 3
   test fixture, fire a control input causing a new highest-severity alert; assert
   `data-testid="detail-new-badge"` is present before any user interaction. Assert the
   badge is absent when the same alert's consecutive count increments without mda_id change.

2. **Consecutive count liveness — no stale memoisation:**
   `consecutive_breach_steps` renders from live API state on each step advance. No
   memoisation or caching that holds a stale count. Observable application state (from
   ADR-014 §Silent Failure 2): advance the scenario; assert `data-testid="detail-consecutive"`
   text matches the current step's `consecutive_breach_steps` value from the API response for
   the top-ranked alert.

3. **Confidence tier is per-step, not cumulative:**
   `getNegotiationLabel(confidence_tier)` renders the current step's confidence_tier for the
   top-ranked alert. The label does not change as a function of consecutive_breach_steps count.
   The intent document must state this explicitly. Observable application state: advance the
   scenario four steps with the same TERMINAL alert persisting; assert that the confidence
   label text is identical at step 1 and step 4 for the same alert (no tier upgrade).

Noted as future design issue (not a separate ADR required):
- Visual styling distinction when consecutive count ≥ threshold (e.g., bold text at ≥3 steps)
  — a styling decision within Zone 1B-detail. No architectural change. File as a design
  follow-on issue when the visual treatment is defined.

---

### 5.2 — PM Agent Ruling Summary

| Question | Ruling | Status |
|---|---|---|
| Q1 — Deduplication (same-indicator multi-entity) | No deduplication; four-level ranking rule with population tiebreak (see §5.3); entity ISO code in detail slot and compact rows | **Resolved in G7** — must appear in intent document |
| Q2 — Causal grouping (cascading alerts) | Mode 3 causal attribution (single line, top alert) unchanged; Zone 1B causal grouping for Mode 1/2 out of scope | **Explicitly deferred** — follow-on ADR required |
| Q3 — Alert storm handling | No summary mode, no count cap; "+N more ↕" confirmed; confidence_tier tertiary sort added to ranking rule | **Resolved in G7**; alert storm visual indicator deferred |
| Q4 — Persistence vs. new-alert distinction | [NEW] = mda_id change only; consecutive count liveness; confidence tier is per-step, not cumulative | **Resolved in G7** — three intent document specifications required; deepening signal is future design issue |

---

### 5.3 — Full Ranking Rule (closes Q1 and Q3 gaps in ADR-014)

ADR-014 §Top-Alert Ranking Rule specifies two sort levels. This section adds two further
tiebreak levels covering the multi-entity and high-confidence-tie cases not present in the
original single-entity design context. The extension fills an unspecified case — it does not
contradict the existing rule. Authority for these tiebreak levels: Section 5 panel deliberation,
2026-06-12. An ADR amendment may be filed if EL directs at review.

**Four-level ranking rule (complete):**

| Level | Sort key | Direction | Rationale |
|---|---|---|---|
| 1 | `severity` | DESC — TERMINAL (0), CRITICAL (1), WARNING (2) | Most urgent finding first |
| 2 | `step_index` | ASC — earliest breach first | Longest consecutive count → strongest argument |
| 3 | `confidence_tier` | ASC — lower number = higher confidence | Most defensible finding ranks above weaker finding at same severity and step |
| 4 | Entity population size | DESC — larger affected population first | Consistent with human cost ledger priority; deterministic tiebreak with semantic motivation |

Stable insertion-order sort applies for any alerts that tie on all four levels.

The detail slot shows the alert ranked first by this rule. The compact list shows all remaining
alerts in the same order.

---

### 5.4 — Deferred Items and Follow-on ADR References

| Item | Reason deferred | Follow-on action |
|---|---|---|
| Zone 1B causal grouping — Mode 1/2 propagation attribution with per-link confidence tier | Layout invariant violation; Mode 1/2 causal inference requires its own confidence tier not displayable in Zone 1B; zone principle assigns causal context to Zone 2 | File follow-on ADR: scope "Zone 1B causal grouping — Mode 1/2 propagation graph attribution with per-link confidence tier disclosure." ARCH number to be assigned from backlog at filing time |
| Alert storm visual indicator — colored active-alert count pill in Zone 1B-compact header at threshold | New layout element; requires design specification (threshold value undefined); ADR amendment required | File follow-on ADR amendment to ADR-014 when threshold and visual treatment are defined |
| Deepening signal — visual badge or indicator when a TERMINAL/CRITICAL alert's consecutive count increments | No architectural change required; pure styling decision; badge vocabulary must stay narrow | File follow-on design issue (not ADR) when visual treatment is defined |

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

**EL approval:** Pending

> {EL approval statement — to be filled at approval time}
> — @PublicEnemage ({date})
