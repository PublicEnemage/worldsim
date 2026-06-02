# WorldSim Milestone Runbook

This runbook defines what a milestone is, how it is created, how work flows through
it, and how it closes. It exists so that milestone ceremonies are consistent across
the project's lifetime — independent of which contributor or agent is running them.

---

## Milestone Definition Standard

A well-formed WorldSim milestone has four properties:

**Single coherent theme.** A milestone answers one question about the simulation:
"Does the engine exist?", "Does the map work?", "Can users run scenarios?".
A milestone that advances multiple independent capabilities simultaneously is not
a milestone — it is a release. Keep the theme narrow enough that the milestone
exit question has a clear yes or no answer.

**Produces working software at every stage.** Each milestone is a vertical slice —
a meaningful capability exists at the end of the milestone that did not exist at the
beginning, and every intermediate state is deployable and testable. A milestone that
is "infrastructure waiting for features" violates this principle.

**Explicit entry and exit criteria.** A milestone is not defined by a list of Issues.
It is defined by the state of the world before it starts and the state of the world
when it ends. Issues are how work gets done within that frame; they are not the frame
itself. If you cannot state the exit criteria before opening the first Issue, the
milestone is not yet well-formed.

**Completable in a defined time horizon.** A milestone that cannot be scoped to a
reasonable time horizon is a project, not a milestone. Decompose it.

---

## Milestone Creation Ceremony

Performed when the previous milestone closes and the next begins.

1. **Create the GitHub Milestone object.** Use the title format
   `Milestone N — Theme Name`. Add a description summarizing the entry criteria
   (what must be true before this milestone begins) and exit criteria (what must
   be true before this milestone can close). Do not set a due date until the
   Engineering Lead has assessed the scope.

2. **Exit checklist auto-created by workflow.** The `milestone-automation.yml`
   workflow fires on milestone creation and automatically opens the exit checklist
   Issue, assigns it to @PublicEnemage, attaches it to the new milestone, and
   applies the `horizon:immediate` label. Verify the Issue was created correctly
   before beginning work.

3. **Scope definition Issue created manually.** Open a separate Issue titled
   `Milestone N scope definition` describing in prose what the milestone will
   build, what it will not build, and what explicit deferrals are being made to
   later milestones. Assign to the milestone. This Issue is closed at the start
   of the milestone, not the end — it is a planning artifact, not a work item.

4. **Known Issues assigned to milestone.** Review the backlog. Assign Issues that
   are clearly in scope for this milestone. Do not over-assign — it is better to
   pull Issues into the milestone during execution than to start with a list that
   is 40% deferred at the end.

---

## Kickoff Gate — Mandatory Before First Implementation Issue

Before any implementation issue is filed for this milestone, the PM Agent
must run the following checks in order:

0. **Milestone metadata alignment check.** Before scope verification begins,
   verify all four milestone artifacts are aligned with the milestone now
   starting as **Current**:
   - GitHub milestone title matches `Milestone N — <Name>` convention
   - GitHub milestone description reflects the core deliverable of the
     milestone now beginning — not a prior or future milestone's scope
   - `CLAUDE.md §What We Are Building First` shows the new milestone as
     current with bullet points matching its core deliverables
   - `CLAUDE.md §Milestone Roadmap` shows the new milestone as Current and
     the next as Next
   Any misalignment found must be corrected before proceeding to step 1.
   (Issue #561)

1. Read `CLAUDE.md` and enumerate every deliverable explicitly named for
   this milestone.
2. Read `docs/roadmap/worldsim-roadmap.md` and enumerate every blocking
   deliverable listed for this milestone.
3. For each named deliverable, verify a corresponding GitHub issue exists
   with: an owner agent named, a `horizon:immediate` or `horizon:near-term`
   label, and the correct milestone assigned.
4. Any named deliverable with no corresponding issue is a
   `scope-gap:untracked` finding. File it as an issue before proceeding.
5. Present the kickoff baseline to the Engineering Lead: a table of all
   named deliverables, their tracking issues, and their owners.

**No implementation begins until this verification is complete and the
Engineering Lead has confirmed the baseline.**

This gate exists because named deliverables can live in prose documents
for an entire milestone without ever becoming tracked work. The gate
converts constitutional scope into board visibility at the moment it
matters — before implementation begins, not at exit review. (NM-019)

---

## Milestone Execution Workflow

**Issues are the unit of work.** Every meaningful change has a GitHub Issue. PRs
reference Issues. The Issue is where the decision to build a thing lives; the PR
is where the code that builds it lives.

**Exit checklist reviewed weekly, not just at the end.** The exit checklist is not
a final gate — it is a live health check. Review it at the start of each work
session and note any blockers. A checklist item that is only checked on the last
day of the milestone is a checklist item that was not managed during the milestone.

**Compliance findings opened as discovered.** Do not accumulate compliance findings
for a batch review at milestone close. Open Issues as findings are encountered.
The milestone-exit compliance scan is a final verification that nothing was missed,
not the primary mechanism for finding violations.

**Architecture decisions made before implementation.** Per `CLAUDE.md § Architecture
Decisions`, no significant feature is implemented without an ADR. The Architect Agent
produces the ADR; Implementation Agents build to the spec. A PR that implements a
significant feature without a referenced ADR does not merge.

---

## Roadmap Update

The roadmap document (`docs/roadmap/worldsim-roadmap.md`) is a mandatory update at every milestone close. This is part of the exit ceremony, not a separate activity.

### When to update
- **Always at milestone close:** Confirm the roadmap accurately reflects the next milestone's scope. If scope has changed, update with a dated rationale note.
- **When a significant scope decision is made mid-milestone:** If an ADR acceptance, a new marquee case, or an EL decision materially changes a future milestone's shape, update the roadmap immediately — do not wait for milestone close.

### How to update
1. Read `docs/roadmap/worldsim-roadmap.md` in full
2. Compare against current SESSION_STATE.md and any scope decisions made since the last revision
3. Update the affected milestone section(s) with the specific change and a dated rationale note
4. Update the revision header: `Last significant revision`, `Next mandatory review`, `Updated against`
5. Commit on a branch, open PR, merge as part of the milestone exit PR or as a companion PR

### What counts as a material change requiring immediate update
- A milestone's core deliverable changes
- A demo anchor moves to a different milestone
- An issue is re-milestoned that affects the milestone's shape (not routine triage)
- An ADR is accepted that changes the sequencing of future work

### What does not require an immediate update
- Routine issue triage within a milestone
- Horizon label changes that don't affect milestone scope
- New issues filed within existing milestone scope

The roadmap is not silently overwritten. Every update includes a dated note explaining what changed and why. The change history is the accountability mechanism.

---

## Issue Disposition Audit

**Performed before the exit checklist is signed off.** This is a blocking gate, not a
retrospective. No milestone may close until every issue assigned to it has been explicitly
dispositioned. (Root: NM-026 — Issue #514 closed COMPLETED without delivery during M9 exit.)

For every issue assigned to the closing milestone:

**If CLOSED/COMPLETED:**
The closure must have one of the following:
- A pull request that references the issue with a closing keyword (`closes #N`, `fixes #N`)
  in the PR body or a commit message.
- An Engineering Lead comment on the issue explaining the non-PR closure. Acceptable
  explanations: "superseded by Issue #N", "addressed in PR #N body (no auto-link)", "manual
  process gate — completion recorded as comment on exit checklist #N", "not-planned because X".
- For epics and parent issues: a comment confirming all child issues are closed.

**If still OPEN:**
Must be explicitly re-milestoned to a future milestone with a brief comment explaining
the deferral, OR closed as NOT_PLANNED with a rationale comment. No issue may remain
in OPEN state against a closing milestone — open issues in a closed milestone are
invisible to future board management.

**The near-miss filing rule:** A near-miss entry that names an issue as an example of a
gap does **not** resolve that issue. Filing NM-020 about Issue #514 did not close Issue
#514. The near-miss documents that the gap was identified; the issue must remain open
until the deliverable it requires is produced. This rule is non-negotiable: near-miss
entries are evidence, not resolutions.

**Board-visibility requirement for manual gates:** Any gate defined in a prose document
(mv-gates.md, SESSION_STATE.md, exit checklist prose, ADR text) that requires Engineering
Lead action before milestone exit must also have a corresponding GitHub issue. Manual
gates without board representation are invisible to board management and have no
exit-checklist hook. Issue creation is part of gate definition, not an optional follow-up.

**Audit record:** Post a comment on the exit checklist issue listing each dispositioned
issue: number, title, disposition type (PR / EL comment / re-milestoned / not-planned).
This comment is the audit trail. The exit checklist may not be signed off until this
comment exists.

---

## Milestone Closure Ceremony

Performed when all exit checklist items are confirmed green **and the Issue Disposition
Audit above is complete.**

1. **Exit checklist fully checked.** Every item in the milestone exit checklist Issue
   is checked. Any item that was skipped has a documented rationale as a comment on
   the Issue. The Engineering Lead adds a final comment: "Exit checklist reviewed and
   complete. Milestone N closes."

2. **Compliance scan recorded in registry.** The Milestone-exit scan entry in
   `docs/compliance/scan-registry.md` exists and references the exit checklist Issue.
   The scan was run against all new code in the milestone. Findings from the scan are
   either remediated or tracked as open Issues with appropriate labels.

3. **Frontend smoke test completed (milestones with frontend deliverables).** Before
   closing a milestone, manually verify in the browser that every frontend feature
   delivered in the milestone is reachable from the UI. Specifically: can a user access
   and operate each new UI component without developer console errors? Backend-only
   verification of API endpoints is insufficient for milestones that include frontend
   deliverables. Document what was tested and confirm it works as a comment on the exit
   checklist Issue. Milestones with no frontend deliverables may skip this step with a
   one-line note confirming that no UI changes were made.

4. **Socratic Agent TEST session completed.** The Engineering Lead has demonstrated
   genuine understanding of the milestone's architectural contributions. This is not
   a formality — it is the checkpoint that ensures the codebase remains governable.

5. **Release tag created.** Tag the merge commit with semantic versioning:
   `v0.N.0` for Milestones 0 through 4 (pre-release). Tag message includes a brief
   description of what the milestone delivered.

6. **Changelog entry written.** Append a milestone summary to `CHANGELOG.md` (create
   if this is the first milestone). Format:
   ```
   ## v0.N.0 — Milestone N: Theme Name (YYYY-MM-DD)
   ### Delivered
   - [bullet list of what was built]
   ### Deferred
   - [bullet list of what was explicitly deferred and to which milestone]
   ### Compliance posture
   - [one-line summary of open finding count by severity]
   ```

7. **Milestone metadata alignment check.** Before the next milestone creation
   ceremony, verify all four artifacts have been updated to reflect this milestone
   as complete and the next as current:
   - GitHub milestone description updated to reflect what shipped and any explicit
     deferrals (with issue numbers and dated rationale)
   - `CLAUDE.md §What We Are Building First` updated to show the next milestone
     as current with correct bullet points
   - `CLAUDE.md §Milestone Roadmap` updated to show the next milestone as Current
   - `docs/roadmap/worldsim-roadmap.md` revision header updated; scope deferrals
     noted with dated rationale
   Any misalignment found must be corrected before step 8. (Issue #561)

8. **Next milestone creation ceremony triggered.** Unless this is the final milestone,
   immediately initiate the creation ceremony for Milestone N+1. Do not leave a gap
   between milestones — the gap is where work loses coherence and Issues accumulate
   without context.

---

## Milestone Governance Review Cadence

Performed once per milestone, in the sequence below. Each phase is grounded
in the output of the previous one — the review cycle moves from concrete
observations to standards revision, not the other way around.

**Phase 1 — Architecture Review** (against current standards)

Run the Architecture Review Facilitator (`Architecture Review: FULL`) against
all ADRs, CLAUDE.md, and the module capability registry for the current
milestone. Findings are implementation gaps (architecture does not meet
standards) and standards gaps (architecture reveals the standards were
underspecified or wrong).

Produces: `ARCH-REVIEW-NNN` in `docs/architecture/reviews/`, GitHub Issues
for all immediate and near-term findings.

**Phase 2 — Finding Disposition**

The Engineering Lead classifies each finding from Phase 1:

- **Implementation gap** — fix the architecture; the standard is correct
- **Standards gap revealed by architecture** — forward to Phase 3 as a
  concrete case; the standard needs revision
- **Genuine design question** — an ADR is required before resolution

This classification determines what goes into Phase 3. Phase 3 is grounded
in specific cases from Phase 2, not in abstractions.

**Phase 3 — Standards and Policy Review** (informed by Phase 2)

Review `docs/CODING_STANDARDS.md`, `docs/DATA_STANDARDS.md`, and
`docs/POLICY.md` against the real implementation experience of the milestone.
Each standards update is traceable to a specific finding from Phase 2 —
no standards revision without a concrete case to anchor it.

Produces: `STD-REVIEW-NNN` in `docs/architecture/reviews/`, updated
standards documents, updated `docs/POLICY.md` where policy positions
are affected.

**Phase 4 — Standards Delta Review**

A quick check: do the Phase 1 architecture fixes still hold against the
Phase 3 updated standards? Usually yes. Occasionally a Phase 3 standards
change reveals that a Phase 1 fix needs refinement. If so, open a new Issue
— do not reopen the Phase 1 finding.

Produces: a brief comment on the ARCH-REVIEW Issue confirming delta review
complete, or a new Issue if refinement is needed.

**Cadence:** Once per milestone, in this sequence. Begin Phase 1 after the
milestone closure ceremony is complete.

**Exception:** A significant new module or policy position may trigger an
out-of-cycle review at any phase independently. Document the trigger in the
review artifact.

---

## Architecture License Framework

Every ADR carries a license status that tracks whether its design decisions
were made against standards that are still in force. An ADR is architectural
debt when the standards it was written against have since changed — it may
describe a valid implementation path that now violates a standard that didn't
exist when it was written.

### License States

**CURRENT** — The ADR was written against standards that remain in force. It
was reviewed at the most recent architecture review cycle. No renewal trigger
has fired. Implementation agents may write code against this ADR and may
write new dependent ADRs.

**UNDER-REVIEW** — The standards the ADR was written against have been updated,
or a renewal trigger has fired. Work under this ADR continues without
interruption — implementation is not blocked. However, no new ADR may be
written as a dependent of an UNDER-REVIEW ADR until the review is complete and
the license is renewed to CURRENT. The period of UNDER-REVIEW must not exceed
one milestone.

**SUPERSEDED** — A newer ADR replaces this one on the same architectural
question. The old ADR remains in `docs/adr/` as a historical record with a
forward reference to its replacement. Superseded ADRs may not be the basis for
new implementation. Their historical record value is preserved.

**REVOKED** — The ADR is no longer valid and the architecture it describes must
not be implemented, extended, or used as the basis for dependent ADRs. REVOKED
status is the drop-everything-and-fix-now case. An open GitHub Issue must
document the revocation reason and the remediation path before REVOKED status
is assigned. Existing implementation based on a REVOKED ADR must be remediated
within the current milestone.

### Renewal Triggers

Each ADR specifies, in its Validity Context section, the standards changes that
would fire a renewal trigger and move the ADR from CURRENT to UNDER-REVIEW.
Renewal triggers are specific and stated up front — general phrases like
"any relevant standard change" are not acceptable. A trigger must name the
specific standard (e.g., `DATA_STANDARDS.md § Units and Measurements`) and
the type of change that would invalidate the ADR's assumptions.

When any standards document is amended, the Engineering Lead reviews all
CURRENT ADRs whose Validity Context lists a matching renewal trigger and
moves affected ADRs to UNDER-REVIEW.

### License Period

The default license period is one milestone. An ADR reviewed at milestone
close is re-licensed for the next milestone. As the architecture stabilizes
and individual ADRs are reviewed across multiple milestones without change,
the Engineering Lead may extend the license period — documented in the ADR's
Validity Context — to two or three milestones. This reduces review overhead
for stable, well-validated decisions.

### The Dependency Rule

**No new ADR may be written as a dependent of an UNDER-REVIEW ADR.**

A dependent ADR builds on the design decisions of its parent. If the parent's
design decisions are under review, the dependent inherits that uncertainty.
Writing a dependent ADR during a parent's review period locks the dependent
to potentially-changing assumptions before the parent review is complete.

The practical consequence: if an Architecture Review moves ADR-001 to
UNDER-REVIEW pending a standards update, any ADR that references ADR-001's
data model (e.g., an ADR defining how the Macroeconomic Module uses
`SimulationEntity.attributes`) must wait until ADR-001 is renewed to CURRENT
before it can be finalized and accepted. Draft work may proceed, but no ADR
may reach Accepted status while its parent is UNDER-REVIEW.

---

## Standards and Policy Review SOP

The Standards and Policy Review is the four-phase process for updating
`docs/CODING_STANDARDS.md`, `docs/DATA_STANDARDS.md`, `docs/POLICY.md`, and
related governance documents. It runs once per milestone, after the
Architecture Review and Finding Disposition phases of the Governance Review
Cadence.

Every standards amendment is traceable to a specific finding from Phase 1 or
Phase 2 of this SOP. No standards revision without a concrete case to anchor it.

**Phase 1 — Domain Council Review**

Activate all Domain Intelligence Council members in CHALLENGE mode against
the full standards suite (`CODING_STANDARDS.md`, `DATA_STANDARDS.MD`,
`POLICY.md`, `CONTRIBUTING.md`) and the Domain Intelligence Council section of
`CLAUDE.md`. Seed the review with findings from the Architecture Review's
Finding Disposition phase that were classified as standards gaps.

Each council member produces Track 1 findings covering:
- Gaps where their framework's concerns are unaddressed in current standards
- Inconsistencies between standards documents
- Policy positions that are incomplete or require updating
- Value dimensions in their council profile that have not been encoded in
  formal standards

Produces: Track 1 findings, one section per council member.

**Phase 2 — Technical Agent Review**

Activate QA Agent, Architect Agent, and Security and Review Agent, informed by
Track 1 findings before beginning. Each agent reviews the full standards suite
from their operational perspective.

**QA Agent** asks: how do I write a test for this? Every standard that cannot be
operationalized into a test is flagged for either a clearer operational
definition or reclassification as a principle rather than a standard.

**Architect Agent** reviews for: ambiguity where two standards together require
an arbitrary implementer choice the standard should have specified, missing
boundary conditions, and architectural contradictions.

**Security and Review Agent** reviews for: standards that create security
vulnerabilities, information exposure risks in provenance requirements,
legal exposure in territorial positions for deployment jurisdictions, and
weakening of the dual-use protection framework.

Produces: Track 2 findings, one section per technical agent.

**Phase 3 — Cross-Track Reconciliation**

Activate QA Agent and Architect Agent to review all Track 1 findings.
Activate Development Economist, Chief Methodologist, and Political Economist
as a representative council sample to review all Track 2 findings.

Each finding receives one of four reconciliation statuses:

- **COMPATIBLE** — consistent with the other track's findings; can be
  implemented as written without modification
- **CONVERGENT** — addresses the same gap as a finding in the other track;
  a single unified amendment satisfies both
- **CONFLICT** — contradicts a finding in the other track; the specific
  contradiction is documented precisely and flagged for Engineering Lead
  decision; no attempt is made to resolve it
- **DEPENDENCY** — assumes an amendment from the other track has already been
  made; the sequencing dependency is documented explicitly

GitHub Issues are created only for COMPATIBLE and CONVERGENT findings.
CONFLICT findings are documented in the review report but not converted to
Issues until the Engineering Lead has dispositioned them in Phase 4.

Produces: `STD-REVIEW-NNN` reconciliation table in
`docs/standards/reviews/STD-REVIEW-NNN-milestone-N.md`.

**Phase 4 — Engineering Lead Synthesis**

The Engineering Lead:
1. Reviews all CONFLICT findings and makes a disposition decision for each:
   accept Track 1, accept Track 2, or propose a third path
2. Approves amendment instructions for all COMPATIBLE, CONVERGENT, and
   resolved CONFLICT findings
3. Updates affected ADR license statuses in Validity Context sections
4. Produces a final synthesis note on the STD-REVIEW issue

**Merge Gate**

No standards amendment reaches `main` until all four phases are complete:
- All CONFLICT findings have been dispositioned by the Engineering Lead
- Cross-track reconciliation is complete (all findings annotated)
- Affected ADR Validity Context sections updated with new license status
- The milestone exit checklist Standards License Audit section is checked

---

## Material Standards Change Definition

A standards change is **material** if a compliant implementation written before
the change would become non-compliant after it. The test is simple: take a
module or data structure that fully satisfies the current standard. Apply the
proposed change. Is it still compliant? If no, the change is material.

Examples of material changes:
- Adding a required field to a data type that existing implementations omit
- Changing a unit convention (e.g., switching canonical currency from constant
  2015 USD to constant 2020 USD) in a way that makes existing stored values
  wrong
- Adding a test requirement that existing modules do not yet satisfy
- Narrowing a type (e.g., `float` → `Decimal` for monetary values) where
  existing code uses the broader type

Examples of non-material changes (no review required):
- Correcting a typo or grammatical error that does not alter the rule
- Adding a cross-reference or example that clarifies existing language without
  changing it
- Adding a new optional field with a documented default
- Adding a new section that covers a domain not previously addressed, where
  no existing implementation is affected

**All material changes require the full review sequence defined below.**
Non-material changes may be made directly with a brief PR description
explaining why the change is non-material. If there is any doubt about
whether a change is material, treat it as material.

---

## Material Standards Change Review Sequence

This sequence applies to any material change to `CODING_STANDARDS.md`,
`DATA_STANDARDS.md`, `POLICY.md`, or `CONTRIBUTING.md`. It is lighter than
the full STD-REVIEW process — targeted at the specific change rather than
the full standards suite — but it is not optional for material changes.

**Steps 3 and 4 must complete before Step 6.** Implementation against a
standard that has not cleared technical and domain review is not permitted.
This sequencing is the primary safeguard against standards changes that are
internally consistent but wrong for the domain or untestable in practice.

### Step 1 — Engineering Lead identifies need

The Engineering Lead documents the proposed change in a GitHub Issue:
- What rule is being added, modified, or removed
- Why the change is needed (concrete case that motivated it, traceable to
  a compliance finding, an ARCH-REVIEW finding, or a specific implementation gap)
- Which standards documents are affected
- Preliminary assessment of materiality

### Step 2 — Draft language prepared

The Engineering Lead or Architect Agent drafts the specific amendment text —
the exact words that will appear in the standards document. The draft is
posted as a comment on the Issue from Step 1. Vague intent is not sufficient;
the draft must be precise enough that a QA Agent can write a test for it.

### Step 3 — Technical Agent Review

QA Agent and Architect Agent review the draft language independently:

**QA Agent asks:** Can I write a test for this? If the rule cannot be
operationalized into a test that can pass or fail, the draft needs a clearer
operational definition or must be reclassified as a principle rather than a
standard. The QA Agent proposes the test(s) that would verify compliance.

**Architect Agent asks:** Is this consistent with existing standards and ADRs?
Does it introduce ambiguity at any boundary? Are there edge cases the draft
does not address that implementers will face?

Both agents post their findings as comments on the Issue. This step is
complete when both agents have posted and the Engineering Lead has read
their findings.

### Step 4 — Domain Council Spot Review

Two or three Domain Intelligence Council members whose frameworks are directly
affected by the proposed change review it in CHALLENGE mode. The Engineering
Lead selects the relevant agents based on the domain of the change:

- Monetary arithmetic changes → Chief Methodologist, Investment Agent
- Human development indicator standards → Development Economist, Intergenerational Advocate
- Governance indicator changes → Political Economist
- Ecological measurement changes → Ecological Economist
- Data provenance or access changes → Geopolitical Analyst, Security lens

The full council review is **not required** for every material standards change.
Targeted spot review of the directly affected frameworks is sufficient for
changes that are material but not sweeping. A sweeping change — one that
affects all four measurement frameworks, alters the fundamental data model,
or changes a cross-cutting rule applied by every module — requires the full
STD-REVIEW process as defined in the Standards and Policy Review SOP above.

When in doubt whether a change is sweeping: if more than three council members'
frameworks are materially affected, treat it as sweeping and run the full process.

### Step 5 — Engineering Lead disposition

The Engineering Lead reviews findings from Steps 3 and 4 and makes one of
three decisions:

- **Approve as drafted** — no significant concerns raised; proceed to Step 6
- **Approve with modifications** — findings require adjustments to the draft;
  post the revised text as a follow-up comment on the Issue before proceeding
- **Reject** — the proposed change has problems that cannot be resolved with
  minor modifications; document the reason and close the Issue

### Step 6 — Implementation against reviewed standards

Once Steps 3 and 4 are complete and the Engineering Lead has approved (Step 5),
implementation may proceed. PRs implementing the standards change include:
- The updated standards document text
- New or updated tests verifying compliance with the new rule
- Any CODING_STANDARDS.md docstring or annotation updates required

### Step 7 — Compliance scan

After the implementing PR merges, run a targeted compliance scan against any
existing code affected by the change. Record the scan in
`docs/compliance/scan-registry.md` with trigger type `Manual` and scope
limited to the affected modules. Findings follow the standard compliance
finding Issue process.

### Step 8 — ADR impact review against renewal triggers

For each CURRENT ADR, check whether the standards change fires any renewal
trigger listed in that ADR's Validity Context section. This check is the
Engineering Lead's responsibility and must be completed within the same
milestone as the standards change.

If a trigger fires: move the affected ADR(s) from CURRENT to UNDER-REVIEW
and open a GitHub Issue documenting the specific trigger and the review
required. The UNDER-REVIEW period must not exceed one milestone.

If no trigger fires: document the negative check result as a comment on the
standards change Issue. "Checked ADR-001 and ADR-002 renewal triggers —
no triggers fire" is sufficient. The check must be recorded; silence is
not evidence of a check.

### Step 9 — ADR license renewals

If any ADR was moved to UNDER-REVIEW in Step 8, complete the review and
renew to CURRENT before the milestone closes. If the review cannot be
completed within the milestone, document the UNDER-REVIEW rationale in the
milestone exit checklist per the Standards License Audit section.

### Step 10 — Scan registry update

Update `docs/compliance/scan-registry.md` to reflect the completed review
sequence. The entry should reference the Issue from Step 1 and note the
final compliance posture of affected modules.

---

## Milestone Definition Table

WorldSim milestone sequence, themes, and current status. Full entry/exit criteria for each
milestone are recorded in the corresponding GitHub milestone description and exit checklist
issue. See `docs/roadmap/worldsim-roadmap.md` for the forward roadmap.

| # | Theme | GitHub Title | Status |
|---|---|---|---|
| 0 | Foundation | Milestone 0 — Foundation | **Complete** |
| 1 | Simulation Core | Milestone 1 — Simulation Core | **Complete** |
| 2 | Geospatial Foundation | Milestone 2 — Geospatial Foundation | **Complete** |
| 3 | Scenario Engine | Milestone 3 — Scenario Engine | **Complete** |
| 4 | Human Cost Ledger | Milestone 4 — Human Cost Ledger | **Complete** |
| 5 | Calibration and Uncertainty | Milestone 5 — Calibration and Uncertainty | **Complete** |
| 6 | Backtesting Coverage Expansion | Milestone 6 — Backtesting Coverage Expansion | **Complete** |
| 7 | Technical Foundation | Milestone 7 — Technical Foundation | **Complete** |
| 8 | Ecological and Governance Frameworks | Milestone 8 — Ecological and Governance Frameworks | **Complete** |
| 9 | Standards Foundation | Milestone 9 — Standards Foundation | **Complete** |
| 10 | Engine Integrity and Instrument Delivery | Milestone 10 — Engine Integrity and Instrument Delivery | **Current** |
| 11 | Engine Investigation and Political Economy | Milestone 11 — Engine Investigation and Political Economy | Upcoming |
| 12 | Active Control and External Sector | Milestone 12 — Active Control and External Sector | Upcoming |
| 13 | Methodology Publication | Milestone 13 — Methodology Publication | Upcoming |

---

## References

- `CLAUDE.md` — project mission, guiding principles, and architecture overview
- `docs/COMPLIANCE.md` — compliance workflow and exception process
- `docs/compliance/scan-registry.md` — compliance scan history
- `docs/templates/milestone-exit-checklist.md` — the template used to generate exit checklist Issues
- `.github/workflows/milestone-automation.yml` — workflow that auto-creates exit checklist Issues on milestone creation
