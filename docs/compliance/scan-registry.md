# WorldSim Compliance Scan Registry

## Purpose

Every compliance scan is a recorded event in this registry. The registry provides:

**Auditability** — a durable record of when scans ran, what scope they covered, and
what they found. Institutional memory that survives session boundaries, contributor
changes, and the passage of time between milestones.

**Trend tracking** — findings are recorded by count and severity. Over successive scans,
the trend line shows whether the compliance posture is improving or deteriorating.
An increasing finding count across milestones is a signal that the standards are not
being applied during development, not just during reviews.

**Gap detection** — the registry makes it visible when a module or subsystem has never
been scanned. A module that appears in the codebase but never in the Scope column is a
blind spot. Gap detection is one of the primary motivations for the registry — absences
are as important as findings.

**Milestone exit gate** — a milestone exit scan must appear in this registry before a
milestone exit checklist can be signed off. The checklist references this registry
explicitly. A milestone that closes without a scan entry is a milestone that closed
without verifying its compliance posture.

---

## Scan Registry

| Scan ID | Date | Trigger | Scope | Findings Summary | Issues Created | Status |
|---|---|---|---|---|---|---|
| SCAN-001 | 2026-04-15 | Manual | ADR-001 initial implementation: `backend/app/simulation/engine/models.py`, `backend/tests/unit/test_models.py` checked against `CODING_STANDARDS.md` and `DATA_STANDARDS.md` | 2 Major (1 Exception #9, 1 Remediate #10), 5 Minor open (F03/F04 #11, F05 #12, F06 #13, F08 #14), 1 Minor resolved in PR #1 (F07) | #9, #10, #11, #12, #13, #14 | Open-findings |

---

## Scan Triggers

Four triggers require or may produce a compliance scan. Each produces an entry in
this registry.

### Automated (every PR — limited scope)

Every pull request triggers a machine-automated compliance check via the CI
`compliance-scan` job (`.github/workflows/ci.yml`). This scan covers
machine-detectable violations only:

- Bare `except` clauses (`E722`)
- Ambiguous variable names (`E741`)
- Legacy typing imports (`Dict`, `List`, `Optional`, `Tuple`, `Set` from `typing`)
- Float literals adjacent to monetary terminology in `backend/app/simulation/`
  (emits `COMPLIANCE-WARN`, not a build failure — requires human judgment)

Automated PR scans do not produce registry entries unless they surface a finding
that requires a compliance finding Issue. They are a preventive control, not an audit.

### Milestone-Exit (required before milestone closes)

A full-scope compliance scan covering all code introduced or modified during the
milestone. Required before the milestone exit checklist can be signed off. Scope
includes all new modules, their tests, and any changed interfaces.

A milestone-exit scan **must** appear in this registry before the exit checklist
Issue is closed. The exit checklist explicitly references the scan ID.

### Quarterly (governance audit)

A governance-level audit conducted every three months. Scope includes:

- Review of all open compliance finding Issues for expired exception review dates
- Review of all deferred findings past their target dates
- Standards review: have any rules become obsolete or counterproductive?
- Exception reconsideration: are accepted exceptions still warranted?
- Pattern analysis: are the same classes of finding recurring?

The quarterly audit produces a summary Issue documenting the current compliance posture.

### Manual (ad hoc)

Triggered by the Engineering Lead or as a consequence of a significant architecture
change (new module, major refactor, new data pipeline). Documents what was scanned,
why the scan was triggered, and what was found.

A manual scan that produces findings follows the standard compliance finding Issue
process. A clean manual scan is recorded in the registry as confirmation of the
reviewed module's compliance posture at that point in time.
