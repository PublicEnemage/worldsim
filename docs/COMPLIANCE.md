# WorldSim Compliance Management Workflow

## Purpose and Governing Principle

WorldSim exists to give vulnerable governments the same quality of analytical
capability that sophisticated financial actors already have. A core part of
that mission is methodological transparency — users can inspect, challenge,
and trust the tool's assumptions because those assumptions are declared and
documented.

**The tool must practice what it preaches.**

The coding and data standards in this repository are not aspirational. They
exist because specific classes of error — float monetary rounding, silent
exception swallowing, vintage dating violations, dimensional conversion
failures, seasonal calendar errors — produce plausible-looking wrong outputs
that mislead users without any visible signal. A WorldSim that doesn't follow
its own standards is a WorldSim that produces the kind of confident-but-wrong
outputs it was built to expose in others.

This document governs what happens when a deviation from WorldSim's standards
is found. The workflow is not punitive. Standards are occasionally wrong,
and the code is occasionally right. Both cases are handled. The requirement
is that deviations are tracked, dispositioned honestly, and either fixed or
accepted with a documented rationale that acknowledges the actual risk.

A deviation that is discovered and handled through this workflow is better
than a deviation that is silently rationalized or buried. The audit trail is
the integrity mechanism.

---

## Finding Classification and Severity

Every compliance finding is classified as Critical, Major, or Minor based on
the nature and consequence of the deviation, not on who found it or where in
the codebase it appears.

### Critical

**Definition:** Produces wrong outputs without a visible error signal, or
violates a contract whose failure mode is invisible to the user.

A Critical finding means the system will appear to work correctly while
producing incorrect results. The user receives a plausible-looking wrong
answer. There is no exception thrown, no log entry, no indicator that anything
went wrong.

**Examples from WorldSim's standards:**

- `float` used for monetary arithmetic — rounding errors accumulate across
  simulation steps and compound into a meaningful error in debt sustainability
  outputs with no warning signal (CODING_STANDARDS.md § Monetary Arithmetic)

- Bare `except` or `except Exception` with silent fallback — a failed exchange
  rate lookup returns 1.0 instead of raising an error; the simulation continues
  with a wrong rate (CODING_STANDARDS.md § Exception Handling)

- Post-vintage data used in backtesting seed — a backtesting case uses a
  revised GDP figure published two years after the scenario start date,
  making the historical validation meaningless (DATA_STANDARDS.md §
  Backtesting Integrity Rules)

- UTF-8 decoding with `errors="ignore"` or `errors="replace"` — source data
  corruption is silently absorbed; the simulation processes corrupted data
  without any signal (DATA_STANDARDS.md § Character Encoding)

- `UnitError` caught and suppressed in a conversion pipeline — an incompatible
  dimensional conversion is silently coerced rather than raising an error
  (DATA_STANDARDS.md § Dimensional Safety)

**Disposition options for Critical:** Remediate only. Exceptions to Critical
findings require explicit project maintainer approval, documented risk
acknowledgment, and a mandatory review date. Critical findings may not be
Deferred.

### Major

**Definition:** Violates an architectural contract in a way that affects
correctness or system integrity over time, but does not produce immediately
invisible wrong outputs.

A Major finding creates risk that may materialize later, makes the system
harder to maintain correctly, or violates a contract that other components
depend on.

**Examples from WorldSim's standards:**

- Public method without type hints — Ruff/mypy cannot enforce type correctness;
  callers may pass incorrect types that fail at runtime rather than at the
  static analysis boundary (CODING_STANDARDS.md § Type Hints)

- Public method without a test — behavior is unverified; refactoring may
  break this method silently; the human cost ledger test requirement is
  specifically a Major finding if human-cost-affecting code paths are untested
  (CODING_STANDARDS.md § Testing Requirements)

- Monetary value stored as raw `Decimal` without `MonetaryValue` type — price
  basis and currency code are not recorded; cross-country comparisons may mix
  nominal and real values silently (DATA_STANDARDS.md § Currency and Monetary
  Value Standards)

- `SimulationModule.compute()` mutates `SimulationState` rather than returning
  Events — breaks deterministic replay, prevents parallel module execution,
  undermines backtesting integrity (ADR-001, CODING_STANDARDS.md §
  Agent Team Workflow Standards)

- Significant interface change without an ADR — the decision and its
  alternatives are not recorded; future contributors relitigate the decision
  (CODING_STANDARDS.md § ADR Requirements)

- Diagram not updated in the same commit as an interface change — the diagram
  diverges from the code and becomes misleading documentation
  (CODING_STANDARDS.md § Diagram Standards)

**Disposition options for Major:** Remediate or Exception (with approval).
Defer is available with a documented target date. Exception on a Major
finding requires senior contributor approval and a review date.

### Minor

**Definition:** Violates style or documentation standards without correctness
or architectural impact.

**Examples from WorldSim's standards:**

- Test function not following `test_[what it does]_[under what condition]`
  naming pattern (CODING_STANDARDS.md § Naming Conventions)

- Docstring missing Google-style structure or Args/Returns sections
  (CODING_STANDARDS.md § Docstrings)

- Commit message not in Conventional Commits format (CODING_STANDARDS.md
  § Commit Message Format)

- `Optional[T]` written instead of `T | None` in Python 3.10+ code
  (CODING_STANDARDS.md § Type Hints)

- Percentage-scale ratio stored internally (e.g. `8.2` for 8.2%) rather than
  decimal fraction (`0.082`) — a presentation-layer value in the simulation
  layer (DATA_STANDARDS.md § Ratios and Rates)

**Disposition options for Minor:** Remediate, Exception, or Defer.
Minor exceptions and deferrals do not require approval beyond the finding owner.

---

## Three Disposition Paths

### 1. Remediate

**What it means:** The code will be changed to comply with the standard.

**When to use:**
- Default for all Critical findings
- Required for Major findings absent an approved exception
- The right disposition when the violation was an oversight and the fix is
  tractable

**Process:**
1. Open a compliance finding Issue using the template, marking disposition
   as Remediate
2. Open a pull request referencing the Issue
3. The PR implements the fix and must pass CI (including the backtesting suite)
4. The PR description includes a brief note confirming the specific rule from
   the standard that the fix satisfies
5. Merge closes the Issue; the finding is recorded as resolved in the audit
   trail

**No exceptions:** A "remediated" finding that still violates the standard
is not remediated. The PR reviewer is responsible for verifying that the
fix actually satisfies the quoted rule in the finding.

### 2. Exception

**What it means:** The code will not be changed. The deviation is acknowledged,
its risk is documented, and it is accepted for explicitly stated reasons.

**When to use:**
- A third-party library returns a non-compliant type (e.g., a data source
  library returns `float`) and wrapping every return value is disproportionate
  to the actual risk
- The rule does not account for a genuinely specific case that the standard's
  authors did not anticipate
- A performance constraint makes compliance not feasible — with measurement
  data showing the constraint is real, not assumed

**Not acceptable as exception rationale:**
- "It works fine in practice" — silent errors by definition appear to work fine
- "It would take too long to fix" — that is a deferral, not an exception
- "The standard seems overly strict here" — use the standard amendment process

**Exception process:**

1. Open a compliance finding Issue, marking disposition as Exception
2. Complete the Exception Rationale and Risk Acknowledgment sections in full
3. For Critical findings: tag the project maintainer for explicit approval
4. For Major findings: tag a senior contributor for approval
5. The approver reads the Risk Acknowledgment, confirms they understand
   what risk is being accepted, and adds their approval note to the Issue
6. Set an Exception Review Date — exceptions are not permanent. The default
   review interval is 6 months for Critical exceptions, 12 months for Major,
   24 months for Minor
7. At the review date, the exception is re-evaluated: has the third-party
   library been updated? Has the constraint been resolved? Is the exception
   still warranted?

**Exceptions are visible.** The `compliance:exception` label on an Issue is
not a mark of shame — it is a mark of honesty. A team that acknowledges its
deviations and documents their rationale is more trustworthy than a team that
pretends deviations don't exist.

### 3. Defer

**What it means:** The finding is valid, will be remediated, but not now.

**When to use:**
- The fix requires architectural work that should be scoped separately
- The finding was discovered mid-sprint and remediation would disrupt
  in-progress work
- The finding is Minor and is being batched with related technical debt

**Not available for Critical findings.** A Critical deviation produces
wrong outputs. It cannot be safely deferred.

**Deferral process:**

1. Open a compliance finding Issue, marking disposition as Defer
2. Set a mandatory target resolution date — not "next sprint" but a specific
   `YYYY-MM-DD`
3. Add any interim mitigating controls to the Remediation Notes section
4. Apply the `compliance:deferred` label
5. At the target resolution date, the Issue is converted to a Remediate
   disposition and a PR is opened. If the date passes without action, the
   finding escalates: Minor becomes Major, Major becomes Critical

**Deferrals are not deferrals forever.** A finding that rolls over its
target date without action or explicit re-deferral with updated rationale
is treated as an escalation.

---

## Exception Approval Process

### Required Fields for All Exceptions

Before an exception is approved, the Issue must contain:

1. **Standard violated** — exact quote of the rule, with section reference
2. **Location** — file, line, function
3. **Exception Rationale** — specific, honest, does not use forbidden rationale
   patterns
4. **Risk Acknowledgment** — what wrong output or failure mode does this risk?
   Under what conditions? Would the user see the error or receive a wrong answer?
5. **Target review date** — not permanent; default intervals apply
6. **Approver acknowledgment** — the approver explicitly states they have read
   the risk section and understand what they are accepting

An exception that is missing any of these fields is not approved, regardless
of who signs it.

### Approval Authority

| Severity | Approver Required |
|---|---|
| Critical | Project maintainer |
| Major | Senior contributor or project maintainer |
| Minor | Finding owner (self-approval permitted) |

Approval is documented in the GitHub Issue by the approver's comment using
the format:

```
EXCEPTION APPROVED
Approved by: @handle
Date: YYYY-MM-DD
Review date: YYYY-MM-DD
I have read the Risk Acknowledgment above. I understand that [brief
restatement of the specific risk being accepted] and accept this deviation
under the stated rationale.
```

A terse "LGTM" is not an approval. The approver must demonstrate that they
have actually read and understood the risk section.

### Exception Review

At each exception's review date, the owner assesses:

1. Has the condition that justified the exception changed?
   (Library updated, constraint resolved, workaround now tractable?)
2. Has the risk materialized? (Has a wrong output been observed that is
   traceable to this deviation?)
3. Is the exception still warranted under the same rationale?

If the exception is renewed, update the Issue with a new review date and note.
If the exception is no longer warranted, convert to a Remediate disposition
and open a PR. If the risk has materialized, treat as a Critical finding
regardless of original severity classification.

---

## Standard Amendment Process

Sometimes the code is right and the standard is wrong. This is expected —
the standards were written before all edge cases were encountered.

**The amendment process is not a way to make violations disappear retroactively.**
It is for cases where the standard genuinely did not account for something,
a better approach exists, or experience has shown the rule is counterproductive.

### When to Use the Amendment Process

- The finding reveals that the standard's rule produces worse outcomes than
  the deviation in this specific class of cases
- A new library, framework, or Python version has rendered a specific rule
  obsolete or suboptimal
- Practical experience running the simulation shows a rule creates overhead
  disproportionate to the risk it mitigates

### When Not to Use It

- The standard is inconvenient — inconvenience is not grounds for amendment
- One team member disagrees with the rule — disagreement is handled through
  discussion, not by opening an amendment to win an argument
- The violation already happened and amendment would retroactively excuse it —
  the finding stands; the amendment applies going forward

### Amendment Process

1. Open a GitHub Issue titled `STANDARD AMENDMENT: [standard doc] § [section]`
2. State the current rule (quoted exactly)
3. State what experience or evidence has shown about its application
4. Propose the amended rule
5. Identify any existing findings or code that would be affected by the
   amendment
6. The amendment is discussed in the Issue comments; consensus of senior
   contributors required
7. If approved: update the standard document in a PR with the message format
   `docs(standards): amend [section] — [one-line rationale]`
8. Existing findings affected by the amendment are re-evaluated against
   the new rule

Amendments are recorded in a change log at the end of each standard document.
The amendment process is how the standards improve over time without losing
the audit trail.

---

## Audit Trail Requirements

### What the Audit Trail Is

The GitHub Issues list, filtered by the `compliance` label family, is the
compliance audit trail. It is not a separate document — it is the live record
of every finding discovered, how it was dispositioned, who approved exceptions,
and what the current status is.

### What Must Be Traceable

For every compliance finding that has been opened:
- The specific violation (quoted rule, file, line)
- When it was discovered and by whom
- The disposition chosen (Remediate / Exception / Defer)
- For Remediate: the PR that resolved it and the date merged
- For Exception: the full rationale, risk acknowledgment, approver, approval
  date, and review date
- For Defer: the target date and any interim mitigations

### Label Conventions

Issues are labeled with the appropriate severity and disposition label:

| Label | Color | Meaning |
|---|---|---|
| `compliance:critical` | Red | Critical finding — produces silent wrong outputs |
| `compliance:major` | Orange | Major finding — violates architectural contract |
| `compliance:minor` | Yellow | Minor finding — style or documentation violation |
| `compliance:exception` | Blue | Exception disposition approved |
| `compliance:deferred` | Grey | Deferred with a target resolution date |

A finding Issue carries both a severity label and, once dispositioned, a
disposition label. A Critical finding that is exceptioned carries both
`compliance:critical` and `compliance:exception`.

### Periodic Audit

The compliance audit trail is reviewed at the start of each milestone.
The review checks:
- Are all open Critical findings either in active remediation or carrying
  a valid, approved exception with a review date that has not passed?
- Have any exception review dates passed without renewal or resolution?
- Are any deferred findings past their target dates?
- Are there patterns in findings that suggest a systematic gap — a module
  or data pipeline that repeatedly produces the same class of finding?

The milestone-start audit produces a brief summary Issue that documents
the current compliance posture. This summary is not a report for external
audiences — it is a project health check for the team.

---

## The Relationship Between This Workflow and CI

CI enforces the rules that can be machine-checked:

- Ruff reports style and type-hint violations
- mypy reports type errors
- pytest reports test failures
- The backtesting suite reports fidelity regressions
- The `compliance-scan` CI job (`.github/workflows/ci.yml`) runs on every PR
  and catches bare `except` clauses, ambiguous variable names, legacy typing
  imports, and emits `COMPLIANCE-WARN` for float literals adjacent to monetary
  terminology

CI failures are not compliance findings — they are build failures that block
merge. The compliance workflow handles deviations that CI cannot detect:
wrong conceptual approaches (float used correctly as float but not as
Decimal-required monetary arithmetic), missing ADRs, vintage dating violations
in backtesting seed data, semantic misuse of types that passes static analysis.

The compliance workflow is not a substitute for CI. It is the human judgment
layer that catches what automated analysis cannot.

---

## Compliance Scan Registry

Every compliance scan — automated or manual — that surfaces findings is
recorded in `docs/compliance/scan-registry.md`. The registry provides:

- An audit trail of when scans ran and what they covered
- Trend tracking across milestones (findings increasing or decreasing?)
- Gap detection — modules that have never been scanned are visible absences

**A milestone exit checklist cannot be signed off until a Milestone-exit scan
entry exists in the registry for that milestone.** The exit checklist explicitly
references the scan ID. A milestone that closes without a registry entry closed
without verifying its compliance posture.

The manual compliance scan script (`backend/scripts/compliance_scan.py`) is the
tool used for milestone-exit reviews and quarterly audits. Run it with:

```bash
python scripts/compliance_scan.py --scope full
```

---

## Milestone Exit Checklist

Every milestone has an exit checklist Issue generated automatically when the
milestone is created in GitHub (via `.github/workflows/milestone-automation.yml`).
The template is at `docs/templates/milestone-exit-checklist.md`.

The exit checklist is the compliance workflow's integration point with the
milestone lifecycle:

- All Critical findings must be remediated or exceptioned before the checklist closes
- All Major findings must be remediated or exceptioned with review dates
- All Minor findings must have open Issues with labels
- The compliance scan registry must have a Milestone-exit entry

See `docs/MILESTONE_RUNBOOK.md` for the complete milestone closure ceremony.
