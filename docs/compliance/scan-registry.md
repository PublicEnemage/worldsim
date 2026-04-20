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
| SCAN-002 | 2026-04-16 | Manual | Full architecture review: ADR-001, ADR-002, `CLAUDE.md`, `docs/scenarios/module-capability-registry.md` — all 9 Domain Intelligence Council agents in CHALLENGE mode via ARCH-REVIEW-001 | 24 blindspots: 6 immediate, 9 near-term, 8 long-term; ADR-001 and ADR-002 moved to UNDER-REVIEW; four deferred ADRs (#38–#41) opened for ADR-003 through ADR-006 | #22–#36, #38–#41 | Open-findings |
| SCAN-003 | 2026-04-17 | Manual | Full standards and policy review: `CODING_STANDARDS.md`, `DATA_STANDARDS.md`, `POLICY.md`, `CONTRIBUTING.md`, `CLAUDE.md` Domain Intelligence Council section — all 9 council agents (Track 1) and QA, Architect, Security agents (Track 2) via STD-REVIEW-001 | 32 findings: 5 CONVERGENT (SA-01–SA-05), 14 COMPATIBLE (SA-06–SA-23), 1 CONFLICT C-1 (disposed Option A — scenario tag boundary adopted; Option B deferred to #53), 2 DEPENDENCY; 10 immediate issues created; ADR-001 and ADR-002 Validity Context sections added | #42–#51, #53 | Open-findings |
| SCAN-004 | 2026-04-19 | Manual — SCR-001 implementation | Full scope: 22 files across `backend/app/` and `backend/tests/`. 5 checks: bare-except (E722), ambiguous-variable-names (E741), legacy-typing-imports, dict-str-float-attributes (QA-1 / SCR-001, new check), monetary-float-literals (warn-only). Result: **0 violations, 2 warnings** — both expected: COMPLIANCE-WARN [QA-1] `Relationship.attributes: dict[str, Any]` (ARCH-4 approved exception, SCR-001); COMPLIANCE-WARN [monetary-float] `Relationship.weight: float` (propagation coefficient, not monetary arithmetic) | None — clean scan | Clean |

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
