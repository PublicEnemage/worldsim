# Milestone Exit Ceremony and Retrospective Process

Every milestone exit must complete the following steps in order before the exit checklist issue is closed. Each step is a named, mandatory gate — not a suggestion. The retrospective (§Milestone Retrospective Process below) is also required and follows these steps.

## Step 1 — Open issue audit (GitHub)

Run `gh issue list --milestone "Milestone {N}..."` and confirm that only the exit checklist issue remains open. Every other issue must be explicitly dispositioned — migrated to a future milestone, closed as delivered, or closed with won't-fix rationale — before the exit checklist closes. A milestone that closes with unexplained open issues has not completed its exit ceremony.

## Step 2 — Milestone reference audit

Update the following three documents in the same PR as the exit SESSION_STATE update. They must not be deferred to a follow-up PR:
- `README.md` — release badge, development status table row for the closing milestone, any stale axis/module descriptions
- `CLAUDE.md` — "What We Are Building First" and "Milestone Roadmap" sections: current → closed, next → current
- `docs/roadmap/worldsim-roadmap.md` — milestone registry table (closing milestone → Complete; new milestone → Current); "Where We Are" narrative; current milestone section heading (`*(current)*` → `*(complete)*`); new milestone section added if absent

The roadmap has an explicit currency policy ("updated at every milestone close"). This step is the enforcement mechanism for that policy. M10, M11, M11.5, and M12 all closed without this step — the gap was caught at M13 kickoff and required PR #896 to repair. Near-miss: NM-041.

## Step 3 — SESSION_STATE internal consistency check

Before committing the exit SESSION_STATE update, verify all four of the following:
- [ ] All issue milestone dispositions in the disposition summary match their actual GitHub milestone assignments (run `gh issue view #{N}` to spot-check)
- [ ] The exit checklist issue for the *new* milestone (M{N+1}) is listed in the Open Issues — M{N+1} table with `immediate | M{N+1} gate issue` notation
- [ ] No stale status notes remain (e.g., "EL endorsement is next required action" after the endorsement was recorded; "active work stream" entries for work that completed mid-milestone)
- [ ] Parallel-track relationships (e.g., Process Redesign phases) explicitly state whether they are blocking prerequisites or concurrent tracks for the new milestone

## Step 4 — Fresh session continuity test

After all exit PRs are merged and main is current, run the fresh session test: reading *only* SESSION_STATE.md and CLAUDE.md, ask — "if a new Claude Code session opened tomorrow and was asked to kick off M{N+1}, what wrong assumptions would it make or what dependencies would it miss?" Fix any critical or high gaps in a SESSION_STATE-only PR before declaring the exit ceremony complete. This step is complete only when the test produces no critical or high findings.

**The exit ceremony is the last action of the milestone.** It runs after all feature work is merged, after the release branch is merged to main, after the demo cycle (for even-numbered milestones) is complete, and after the retrospective. It is not a side task to be delegated to a follow-up session.

---

# Milestone Retrospective Process

Every milestone exit ceremony must include a retrospective. The retrospective
is not optional and is not a formality. It is an epistemic discipline — the
same discipline that makes backtesting the primary signal for model improvement
applies here to the development process itself.

## What the Retrospective Covers

Every retrospective addresses three questions, in writing, as a comment on
the exit checklist Issue:

**1. What defects evaded the test suite?**
Name every bug that was caught by manual testing, user report, or visual
inspection rather than by an automated test. For each: what was the defect,
how was it caught, and at what point in development would a test have caught
it earlier?

**2. What process gaps caused them?**
For each defect that evaded testing: what test did not exist that would have
caught it? Was the gap a missing test type (unit, integration, end-to-end),
a missing coverage area, or a test-after rather than test-before discipline
failure? Name the gap specifically — not "we need more tests" but "we had
no Playwright test for the scenario advance → drawer open flow."

**3. What testing improvements are required before the next milestone begins?**
Specific, named deliverables — not intentions. Each improvement is a blocking
requirement for the next milestone exit, not a suggestion. If a testing gap
was identified, the next milestone exit checklist must include a checkbox
confirming the gap was closed.

## The M4 Radar Chart Drawer Incident — Canonical Reference

Canonical incident record: `docs/frontend/testing-standards.md §Anti-Patterns from M4` and `design-decisions.md DD-004`.
