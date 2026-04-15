---
name: Compliance Finding
about: Report a deviation from CODING_STANDARDS.md, DATA_STANDARDS.md, or CONTRIBUTING.md
labels: compliance
---

## Finding Reference

**Finding ID:** CF-<!-- sequential number, e.g. CF-001 -->
**Discovered:** <!-- YYYY-MM-DD -->
**Discovered by:** <!-- agent role or contributor handle -->

---

## Standard Violated

**Standard document:**
<!-- CODING_STANDARDS.md | DATA_STANDARDS.md | CONTRIBUTING.md | POLICY.md -->

**Section reference:**
<!-- e.g. "CODING_STANDARDS.md § Monetary Arithmetic: Decimal, Never float" -->

**Relevant rule (quoted):**
<!--
Paste the exact text of the rule from the standard document.
Do not paraphrase — quoting the rule makes clear what was actually violated
and makes it easy to verify whether a proposed fix satisfies it.
-->

---

## Location in Codebase

**File(s):**
<!-- e.g. backend/app/simulation/modules/macroeconomic.py -->

**Line(s):**
<!-- e.g. Line 142, or Lines 87-103 -->

**Function / class:**
<!-- e.g. FiscalModule.compute() -->

---

## Description of Deviation

<!--
Describe precisely what is wrong. What does the code do? What should it do
instead? Write this so that someone unfamiliar with the file can understand
the finding without reading the code first.
-->

---

## Evidence

<!--
Paste the non-compliant code or data. Use a code block with the language
specified. Include enough surrounding context that the violation is visible.
-->

```python
# paste code here
```

<!--
If the finding is in data or configuration rather than code, paste the
relevant excerpt here.
-->

---

## Severity Classification

**Severity:** <!-- Critical | Major | Minor -->

<!--
Critical: Produces wrong outputs without a visible error signal. Float monetary
arithmetic, silent exception swallowing, dimensional conversion errors,
backtesting integrity violations (using post-vintage data), UTF-8 violations
that corrupt data silently.

Major: Violates an architectural contract in a way that affects correctness or
makes the system harder to maintain without causing immediate wrong outputs.
Missing type hints on public functions, missing tests for a public method,
bare except with logging but no re-raise, missing ADR for a significant
interface change, monetary values without MonetaryValue type.

Minor: Violates style or documentation standards without correctness impact.
Test function name not following test_[what]_[condition] pattern, docstring
missing or not in Google style, commit message not in Conventional Commits
format, diagram not updated in same commit as interface change.
-->

**Severity rationale:**
<!--
One sentence explaining why this finding deserves this severity classification.
Reference the specific risk the violation creates.
-->

---

## Proposed Disposition

**Disposition:** <!-- Remediate | Exception | Defer -->

<!--
Remediate: The code will be fixed to comply with the standard. Default for all
Critical findings. Required for Major findings absent a documented exception.

Exception: The code will not be changed; the deviation is acknowledged and
accepted for documented reasons. Requires approval for Critical and Major
findings. See exception rationale section below.

Defer: The finding is valid and will be remediated, but not in the current
sprint. Requires a target resolution date. Not available for Critical findings.
-->

---

## Remediation Notes

<!--
If disposition is Remediate: describe how the code will be changed. What
specifically will be done to bring it into compliance? If a PR is already
open, link it here.

If disposition is Exception or Defer: describe any mitigating controls or
partial remediations that reduce the risk of the deviation in the interim.

Leave blank only if no remediation is planned (Exception with no interim
mitigations) and document that explicitly.
-->

---

## Exception Rationale

<!--
Required if disposition is Exception. Leave blank for Remediate or Defer.

Explain why compliance with this rule is not possible or not appropriate in
this specific case. Acceptable exception rationales:
- Third-party library returns float and wrapping is disproportionate to risk
  (Critical/Major: requires explicit approval)
- Standard rule doesn't account for this specific case (may indicate standard
  needs amendment — see COMPLIANCE.md § Standard Amendment Process)
- Performance constraint with documented measurement showing compliance is
  not feasible (Major only; not available for Critical)

Not acceptable as exception rationale:
- "It works fine in practice" — correctness cannot be verified by observation
  for silent errors
- "It would take too long to fix" — this is a deferral, not an exception
- "The standard is wrong" — use the standard amendment process instead
-->

---

## Risk Acknowledgment

<!--
Required for all exception dispositions. Describe:
1. What specific wrong output or failure mode does this deviation risk?
2. Under what conditions would the risk materialize?
3. What would a user observe if the risk materialized — would the error be
   visible or would they receive a plausible-looking wrong answer?

The risk acknowledgment must be honest. "No material risk" is not an
acceptable answer for a Critical finding.
-->

---

## Owner

**Responsible for resolution:** <!-- GitHub handle -->
**Target resolution date:** <!-- YYYY-MM-DD; required for Remediate and Defer dispositions -->

---

## Exception Approval

<!--
Required for Exception disposition on Critical or Major findings.
Leave blank for Minor exceptions and for Remediate/Defer dispositions.

An exception on a Critical finding requires explicit approval from the
project maintainer. An exception on a Major finding requires approval from
a senior contributor. Approver must acknowledge the risk section above.
-->

**Approved by:** <!-- GitHub handle of approver -->
**Approval date:** <!-- YYYY-MM-DD -->
**Exception review date:** <!-- YYYY-MM-DD; exceptions are not permanent — set a review date -->
**Approval note:**
<!--
The approver's statement that they have read the risk acknowledgment,
understand what risk is being accepted, and authorize the exception.
-->
