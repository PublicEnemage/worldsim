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

## Milestone Closure Ceremony

Performed when all exit checklist items are confirmed green.

1. **Exit checklist fully checked.** Every item in the milestone exit checklist Issue
   is checked. Any item that was skipped has a documented rationale as a comment on
   the Issue. The Engineering Lead adds a final comment: "Exit checklist reviewed and
   complete. Milestone N closes."

2. **Compliance scan recorded in registry.** The Milestone-exit scan entry in
   `docs/compliance/scan-registry.md` exists and references the exit checklist Issue.
   The scan was run against all new code in the milestone. Findings from the scan are
   either remediated or tracked as open Issues with appropriate labels.

3. **Socratic Agent TEST session completed.** The Engineering Lead has demonstrated
   genuine understanding of the milestone's architectural contributions. This is not
   a formality — it is the checkpoint that ensures the codebase remains governable.

4. **Release tag created.** Tag the merge commit with semantic versioning:
   `v0.N.0` for Milestones 0 through 4 (pre-release). Tag message includes a brief
   description of what the milestone delivered.

5. **Changelog entry written.** Append a milestone summary to `CHANGELOG.md` (create
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

6. **Next milestone creation ceremony triggered.** Unless this is the final milestone,
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

The five WorldSim milestones, their themes, entry criteria, and exit criteria.

| # | Theme | Entry Criteria | Exit Criteria | Status |
|---|---|---|---|---|
| 0 | Foundation | Repository created | CI/CD pipeline active; ADR-001 accepted; CLAUDE.md, CODING_STANDARDS.md, DATA_STANDARDS.md, CONTRIBUTING.md committed; technology stack verified | **Complete** |
| 1 | Simulation Core | Milestone 0 complete | Country entity data model implemented per ADR-001; basic event propagation graph working; annual timestep engine running; World Bank seed data loaded for at least 10 countries; simulation output verified through CLI and unit tests; no UI required | **In Progress** |
| 2 | Geospatial Foundation | Milestone 1 complete | PostGIS database with country boundary GeoJSON (Natural Earth); FastAPI layer serving country data; MapLibre GL frontend rendering one variable as choropleth; the map renders correctly in browser; one variable, no scenarios yet | Upcoming |
| 3 | Scenario Engine | Milestone 2 complete | User-defined scenario configuration; time acceleration controls; comparative scenario output; first backtesting run against one documented historical case (Greece 2010–2012 or Thailand 1997) with fidelity thresholds defined and CI-enforced | Upcoming |
| 4 | Human Cost Ledger | Milestone 3 complete | Cohort-level demographic module active; multi-currency measurement output (Financial, Human Development, Ecological, Governance simultaneously); Minimum Descent Altitude threshold system firing alerts; radar chart dashboard displaying all four dimensions with equal visual weight | Upcoming |

---

## References

- `CLAUDE.md` — project mission, guiding principles, and architecture overview
- `docs/COMPLIANCE.md` — compliance workflow and exception process
- `docs/compliance/scan-registry.md` — compliance scan history
- `docs/templates/milestone-exit-checklist.md` — the template used to generate exit checklist Issues
- `.github/workflows/milestone-automation.yml` — workflow that auto-creates exit checklist Issues on milestone creation
