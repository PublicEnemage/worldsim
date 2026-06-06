# Legibility Metrics Dashboard — Definition and Process

> **Status:** Active — M12 onward
> **Origin:** Issue #259 (CTO legibility metrics dashboard — ongoing pulse tracking)
> **Prerequisites:** Issue #255 (baseline capture — complete, M7), Issue #256 (North Star amendment),
> Issue #257 (blind audit process), Issue #258 (intent blocks)
> **Related document:** `docs/standards/legibility-baseline-m7.md` (M7 quantitative baseline)

---

## Purpose

Legibility is a property of the codebase that drifts unfavorably under velocity pressure
in the same way test coverage drifts without enforcement. This document defines the four
tracked Tier 1 metrics, the Tier 2 semi-automated process metrics, the Tier 3 qualitative
leading indicators, and the tolerance thresholds reviewed at each milestone exit.

All metrics serve the Legibility North Star (Issue #256): code must be modifiable by an
intermediate developer without access to authorial context. When metrics drift red, the
question is not "which rule was violated" but "would an intermediate developer be able to
safely modify this module?"

---

## Metric Tiers

### Tier 1 — Automated (CI)

These four metrics are computed automatically on every milestone exit as part of the CI
pipeline and appended to `docs/standards/legibility-baseline-m{N}.md`.

#### Metric 1.1 — Mean Cognitive Complexity per Module (Python)

**Tool:** `radon` (pinned: `radon==6.0.1` in `backend/requirements.txt`)
**Scope:** `backend/app/` — all `.py` files; exclude `__init__.py` and generated files
**Command:**

```bash
cd backend
radon cc app/ -s -a --min A
```

**Grade thresholds:**

| Grade | Cyclomatic complexity range | Legibility gate |
|---|---|---|
| A | 1–5 | Pass |
| B | 6–10 | Pass |
| C | 11–15 | Warning — document in baseline; must not grow |
| D | 16–24 | Fail — must reduce before milestone exit |
| E/F | 25+ | Fail — hard block |

**Pass condition:** No D, E, or F grade blocks at milestone exit. C-grade count must
not increase from the prior milestone baseline.

**Deviation rule:** If a C-grade or above block cannot be reduced before milestone exit,
the Engineering Lead must document the block by name, file, and complexity score in the
milestone baseline document with an explanation. Undocumented C+ blocks are a compliance
finding.

#### Metric 1.2 — p90 Function Length in Lines per Module

**Tool:** `radon raw` (included in same `radon` package)
**Command:**

```bash
cd backend
radon raw app/ -s | grep -A5 "LOC"
```

**Thresholds:**

| p90 function length | Status |
|---|---|
| < 40 lines | Green |
| 40–60 lines | Yellow — document in baseline |
| > 60 lines | Red — must be refactored or explicitly deferred |

**Pass condition:** p90 function length below 60 lines across all modules. Functions
exceeding 60 lines that are not flagged in the prior baseline are a compliance finding.

#### Metric 1.3 — Silent Failure Surface Count

**Tool:** `grep` (scripted in CI step)
**Scope:** `backend/app/` — exclude `__init__.py`, `test_*`, `*_test.py`
**Command:**

```bash
cd backend
grep -rn "^\s*return \[\]\|return None\|return {}" app/ \
  --include="*.py" \
  --exclude="__init__.py" \
  | grep -v "test_" \
  | wc -l
```

**Classification:** Not all bare returns are risky. The CI step counts all occurrences;
the milestone baseline document must classify each as a legitimate guard clause or a
higher-risk silent return (no logging, caller may not check). See the M7 baseline
(`docs/standards/legibility-baseline-m7.md §Category 2`) for the classification
methodology.

**Thresholds:**

| Higher-risk silent returns (unlogged, unchecked) | Status |
|---|---|
| Declining vs. prior milestone | Green |
| Same as prior milestone | Yellow — stable; document in baseline |
| Growing vs. prior milestone | Red — each new unlogged silent return requires a filed issue |

#### Metric 1.4 — Test-to-Implementation Line Ratio per Module

**Tool:** `wc -l` (scripted in CI step)
**Scope:** `backend/app/` implementation vs. `backend/tests/` matching test files
**Command:**

```bash
cd backend
# Implementation lines
find app/ -name "*.py" -not -name "__init__.py" -exec wc -l {} + | tail -1
# Test lines
find tests/ -name "*.py" -not -name "__init__.py" -exec wc -l {} + | tail -1
```

**Thresholds (overall ratio):**

| Test-to-implementation ratio | Status |
|---|---|
| ≥ 1.5 | Green |
| 1.0–1.5 | Yellow |
| < 1.0 | Red — test gap; must be addressed before milestone exit |

**Per-module floor:** No individual module may have a test-to-implementation ratio below
0.40 at milestone exit. The `api` module was 0.45 at M7 baseline — improvement toward
0.70 is required.

---

### TypeScript Legibility — ESLint Complexity Rule (Frontend)

**Tool:** ESLint with `complexity` rule (included in `frontend/` ESLint configuration)
**Scope:** `frontend/src/` — all `.ts` and `.tsx` files
**Configuration (add to `frontend/.eslintrc` or equivalent):**

```json
{
  "rules": {
    "complexity": ["warn", { "max": 10 }]
  }
}
```

**Threshold levels:**

| Cyclomatic complexity | ESLint severity | Legibility gate |
|---|---|---|
| ≤ 10 | (no warning) | Pass |
| 11–15 | `warn` | Warning — must not grow; document in baseline |
| > 15 | `error` | Fail — blocks CI |

**CI enforcement:** The frontend lint step already runs `npm run lint`. The `complexity`
rule at `warn` level produces output that is captured in the CI log but does not fail the
build. At `error` level (> 15), the build fails. The milestone exit checklist requires
reviewing all `complexity` warnings and confirming no function exceeds 15.

**Command to run locally:**

```bash
cd frontend
npm run lint 2>&1 | grep "complexity"
```

---

## GitHub Actions CI Steps

### Python Legibility Step (Backend CI Job)

Add the following step to the `test-backend` job in `.github/workflows/ci.yml`, after
the lint step:

```yaml
- name: Legibility — radon cognitive complexity gate
  run: |
    cd backend
    pip install radon==6.0.1
    # Fail if any D/E/F grade blocks exist
    RESULT=$(radon cc app/ -s --min D 2>&1)
    if [ -n "$RESULT" ]; then
      echo "LEGIBILITY GATE FAILED — D/E/F grade blocks found:"
      echo "$RESULT"
      exit 1
    fi
    echo "Legibility gate passed — no D/E/F grade blocks."
  if: needs.changes.outputs.backend == 'true'
```

**Scope note:** This step runs only when `backend/` files change (same `if:` condition
as the existing test steps). It does not run on documentation-only commits.

**Milestone exit supplement:** At milestone exit, run the full complexity report and
append the output to the milestone legibility baseline document:

```bash
cd backend
radon cc app/ -s -a --min A >> docs/standards/legibility-baseline-m{N}.md
```

### TypeScript Legibility Step (Frontend CI Job)

The existing `npm run lint` step in the frontend CI job enforces the ESLint `complexity`
rule. No additional CI step is required if the rule is configured in `.eslintrc`.

To make complexity warnings explicit in the CI log, add:

```yaml
- name: Legibility — TypeScript complexity check
  run: |
    cd frontend
    npm run lint 2>&1 | tee lint-output.txt
    COMPLEXITY_WARNINGS=$(grep "complexity" lint-output.txt | wc -l)
    echo "TypeScript complexity warnings: $COMPLEXITY_WARNINGS"
    if grep -q "complexity.*error" lint-output.txt; then
      echo "LEGIBILITY GATE FAILED — TypeScript functions exceed complexity 15"
      exit 1
    fi
  if: needs.changes.outputs.frontend == 'true'
```

---

## Tolerance Thresholds (Summary Table)

| Metric | Green | Yellow | Red |
|---|---|---|---|
| Python mean cognitive complexity (radon) | Average grade A; no D/E/F blocks | 1–2 C-grade blocks new vs. prior baseline | Any D/E/F block; C-grade count growing |
| TypeScript function complexity (ESLint) | All functions ≤ 10 | 1–3 functions 11–15 (warn) | Any function > 15 (error) |
| Blind audit mean score (Issue #257) | > 3.5 | 2.5–3.5 | < 2.5 |
| Spec-to-test gap count (Issue #258) | Declining | Flat | Growing |
| Silent failure surface (higher-risk) | Declining | Flat | Growing |
| Test-to-implementation ratio (overall) | ≥ 1.5 | 1.0–1.5 | < 1.0 |
| Test-to-implementation ratio (per module) | ≥ 0.70 | 0.40–0.70 | < 0.40 |

---

## Tier 2 — Semi-Automated (Process)

These metrics require a combination of tooling and manual review. They are checked at
each milestone exit as part of the exit ceremony.

### Metric 2.1 — Spec-to-Test Gap Count (Issue #258)

**Definition:** Number of intent blocks (Issue #258 format) in implementation files
that do not have a corresponding test asserting the stated behavior.
**Process:** Identify all `# INTENT:` blocks in `backend/app/`; cross-reference against
test files; count gaps.
**Tracking:** Recorded in the milestone baseline document under "Tier 2 Metrics."
**Threshold:** Gap count must be declining. A flat or growing gap count requires a filed
issue before milestone exit is approved.

### Metric 2.2 — Blind Audit Mean Score (Issue #257)

**Definition:** Mean legibility score (1–5 scale) from the blind code audit protocol
(`docs/process/blind-code-audit-prompt.md`).
**Process:** Conducted at each milestone exit per Issue #257 protocol.
**Threshold:** Mean score > 3.5 is green. Score 2.5–3.5 triggers a root cause analysis.
Score < 2.5 blocks milestone exit until a remediation plan is filed.
**Tracking:** Recorded in `docs/process/blind-audit-m{N}-baseline.md` (see
`docs/process/blind-audit-m7-baseline.md` for M7 reference).

---

## Tier 3 — Leading Indicators (Qualitative)

These are tracked in the milestone baseline document as qualitative assessments, not
automated counts. They are leading indicators: deterioration here predicts Tier 1
metric deterioration in the next 1–2 milestones.

### Indicator 3.1 — Assumption Documentation Rate

**Definition:** Fraction of non-trivial functions that have documented preconditions
(either as `# INTENT:` blocks per Issue #258 or as docstring `Args:` / `Raises:` sections).
**Assessment:** Scan `backend/app/` modules and report the fraction with documented
preconditions at milestone exit. No automated count — Engineering Lead spot-checks
five randomly selected non-trivial functions per module.

### Indicator 3.2 — Implicit Dependency Depth

**Definition:** Functions that depend on module-level state, global configuration, or
database session state that is not declared in the function signature.
**Assessment:** Flagged by the blind audit (Issue #257) and by Architecture Review.
Not automated. Qualitative rating: Low / Medium / High per module.

---

## Milestone Exit Checklist Items

The following items must be added to the milestone exit checklist
(`docs/process/milestone-exit-checklist.md`). They are blocking requirements for
milestone exit — not optional:

```markdown
### Legibility Metrics

- [ ] Radon cognitive complexity gate run against `backend/app/` — no D/E/F grade blocks
- [ ] C-grade block count compared to prior milestone baseline — count must not have grown
      (if grown, each new C-grade block documented by name in milestone baseline)
- [ ] p90 function length checked — no module above 60 lines p90
- [ ] Silent failure surface classified — higher-risk unlogged returns count recorded;
      any increase vs. prior baseline requires a filed issue
- [ ] Test-to-implementation ratio computed per module — no module below 0.40
- [ ] TypeScript ESLint complexity warnings reviewed — zero functions > 15 (error level)
- [ ] Tier 1 metrics recorded in `docs/standards/legibility-baseline-m{N}.md`
      (append to file; do not overwrite prior milestones)
- [ ] Spec-to-test gap count reviewed (Issue #258) — declining or flat with documented plan
- [ ] Blind code audit completed (Issue #257) — mean score ≥ 2.5 to close milestone;
      ≥ 3.5 for green status
- [ ] Engineering Lead reviews legibility dashboard at milestone exit ceremony
- [ ] Any Red metric documented in SESSION_STATE.md with a filed remediation issue
```

---

## Dashboard Review Protocol

The Engineering Lead reviews the legibility dashboard at each milestone exit as part of
the exit ceremony. The review covers:

1. Compare all Tier 1 metrics against the prior milestone baseline
2. Confirm no metric has moved from Green to Red without a filed issue
3. Review Tier 2 metrics (blind audit score, spec-to-test gap) — confirm within tolerance
4. Review Tier 3 qualitative indicators — flag any deterioration as a risk
5. Confirm the new milestone baseline document has been appended
   (`docs/standards/legibility-baseline-m{N}.md`)

If any Tier 1 metric is Red, the milestone exit is blocked until either:
(a) the metric is remediated, or
(b) the Engineering Lead files a documented exception with a remediation plan
    and timeline in SESSION_STATE.md.

---

## Relationship to Other Process Documents

| Document | Relationship |
|---|---|
| `docs/standards/legibility-baseline-m7.md` | M7 quantitative baseline — the first captured snapshot; all subsequent baselines follow its structure |
| `docs/process/blind-audit-m7-baseline.md` | M7 blind audit baseline (Tier 2 Metric 2.2) |
| `docs/process/blind-code-audit-prompt.md` | Protocol for conducting blind code audits |
| `docs/process/intent-block-author-prompt.md` | Intent block authoring protocol (feeds Tier 2 Metric 2.1) |
| `docs/CODING_STANDARDS.md` | Authoritative coding style; legibility metrics enforce the quantitative floor |
| Issue #255 | M7 baseline capture — prerequisite (complete) |
| Issue #256 | North Star amendment — prerequisite |
| Issue #257 | Blind audit process — prerequisite |
| Issue #258 | Intent blocks — prerequisite |

---

*Defined by PM Agent — Issue #259. Metrics reviewed by Engineering Lead at each
milestone exit beginning M8. Dashboard baseline captured at M7 exit (Issue #255).*
