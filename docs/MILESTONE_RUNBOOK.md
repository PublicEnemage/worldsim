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

Milestone Governance Review Cadence:

1. Architecture Review (against current standards)
   — Finds implementation gaps and reveals standards gaps
   — Produces: ARCH-REVIEW-NNN, GitHub Issues

2. Finding Disposition
   — Engineering Lead classifies each finding:
     a. Implementation gap → fix architecture
     b. Standards gap revealed by architecture → input to Step 3
     c. Genuine design question → ADR required

3. Standards and Policy Review (informed by Step 2)
   — Reviews standards against real implementation experience
   — Grounded in specific cases from Step 2, not abstractions
   — Produces: STD-REVIEW-NNN, updated standards documents

4. Standards Delta Review
   — Quick check: do the Phase 1 architecture fixes still hold
     against the Phase 3 updated standards?
   — Usually yes. Occasionally reveals a fix needs refinement.

Cadence: Once per milestone, in this sequence.
Exception: A significant new module or policy position may
trigger an out-of-cycle review at any phase independently.

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
