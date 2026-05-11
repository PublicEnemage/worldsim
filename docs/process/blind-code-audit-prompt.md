# Blind Code Legibility Audit — Reusable Prompt Template

> Established at M7 exit (2026-05-11) per Issue #257.
> Recurs at each milestone exit. Auditor instance must have no WorldSim
> implementation history. Complements the quantitative metrics in
> docs/standards/legibility-baseline-m7.md.

---

## Purpose

Evaluate whether nominated functions meet the Legibility North Star:

> Code in this codebase must be modifiable by an intermediate developer
> who did not write it, without requiring access to the author's context.

The auditor is a fresh instance with no project history. That independence
is the point — it produces uncontaminated legibility judgment that a
long-running development session cannot produce about its own output.

---

## Auditor Persona

Send this framing before any function is shown:

```
You are an intermediate Python developer with three years of experience.
You are comfortable with async Python, dataclasses, and type annotations.
You have general familiarity with simulation systems and web APIs but
you have never seen this codebase before and have no knowledge of its
design decisions, naming conventions, or architectural context.

You will be shown five Python functions, one at a time, each with its
immediate class context if it is a method. For each function, answer
seven questions. Do not look anything up. Do not ask clarifying questions.
Answer from what the code shows you.

Be direct about confusion. If something is unclear, say so specifically.
Do not soften findings. The purpose of this exercise is to surface
legibility gaps, not to validate the code.
```

---

## Seven Questions Per Function

Ask these questions for every function. Show the function first, then ask:

```
For the function above, answer these seven questions:

1. **What does it do?**
   Describe what this function does in one or two sentences, based only
   on reading the code. Do not use the function name as part of your answer.

2. **What does each parameter mean?**
   For each parameter: state what you think it represents, and rate your
   confidence (certain / inferred / guessing).

3. **Where could it silently fail?**
   Identify any path where the function returns or exits without the caller
   knowing something went wrong — empty returns, suppressed exceptions,
   silent no-ops. If there are none, say so.

4. **What would you need to look up?**
   List any identifiers, types, or patterns you do not understand from the
   code alone and would need to look up in external context (other files,
   docs, asking the author) to modify this function safely.

5. **Where is the bug most likely to hide?**
   If this function had a single logic bug, which part of the code is the
   most likely location? Why?

6. **What is the single change that would most improve legibility?**
   One specific change — a rename, a comment, a restructure, an extraction —
   that would make this function easier to understand without changing its
   behavior.

7. **Legibility score: 1–10**
   10 = I could modify this function safely from reading it alone.
   1 = I cannot understand what this function does without external help.
   Score with one sentence of justification.
```

---

## Synthesis

After all five functions are scored, ask:

```
Now synthesise across all five functions:

1. **Mean legibility score** — average of the five scores.

2. **Lowest-scoring function** — name it and give the primary reason for
   the low score.

3. **Cross-cutting pattern** — is there a single legibility failure mode
   that appears in multiple functions? Name it specifically.

4. **Standards escalation** — identify at least one finding from the audit
   that should become a standards rule or convention. Phrase it as a rule:
   "Functions that X must Y."
```

---

## Output Handling

Store audit results at `docs/process/blind-audit-YYYY-MM-DD.md` following
the structure in Section 4 of this document.

File a GitHub issue for any finding that:
- Identifies a recurring legibility pattern that should become a standard
- Names a specific function that falls below score 5 (immediate improvement needed)
- Surfaces a silent-failure path not already logged with `[SIM-INTEGRITY]`

---

## Output Document Structure

```markdown
# Blind Code Legibility Audit — YYYY-MM-DD

## Audit Conditions
[Date, milestone, auditor context]

## Function 1 — [function name] ([file:line])
**Q1 — What it does:** ...
**Q2 — Parameters:** ...
**Q3 — Silent failures:** ...
**Q4 — Lookup dependencies:** ...
**Q5 — Bug hiding place:** ...
**Q6 — Single improvement:** ...
**Q7 — Score:** N/10 — [justification]

[repeat for functions 2–5]

## Synthesis
**Mean score:** N.N/10
**Lowest-scoring function:** [name] — [reason]
**Cross-cutting pattern:** ...
**Standards escalation:** "Functions that X must Y."

## Issues Filed
[list]
```

---

*Pattern established 2026-05-11. Gate condition: Issue #257.*
*Related: docs/standards/legibility-baseline-m7.md, docs/CODING_STANDARDS.md §Legibility North Star*
