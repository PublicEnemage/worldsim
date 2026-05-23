# WorldSim Known Issues Registry

A Known Issue is a confirmed limitation or unreliable behaviour of external
infrastructure, tooling, or third-party services that:

- Has a real, recurrent impact on the development process
- Cannot be fixed by redesigning internal systems or processes
- Has a documented workaround or mitigation procedure

## Distinction from near-misses

**Near-misses** are internal hazards. The response is always a process improvement
that eliminates or structurally reduces the hazard. The countermeasure is never
"be more careful" — it is always "redesign the system so careful isn't required."

**Known Issues** are external limitations. The root cause lies outside the
project's control (GitHub's infrastructure, a third-party API, an OS behaviour).
The response is a documented workaround and awareness — not a process change,
because there is no internal process to change. Filing a Known Issue as a
near-miss would produce a process improvement recommendation against something
we cannot redesign.

When in doubt: if the fix requires changing our own code, process, or documents,
it is a near-miss. If the fix requires waiting for an upstream vendor to change
their system, it is a Known Issue.

---

## KI-001 — GitHub Actions: `pull_request` Event Silently Fails to Fire

**Date first observed:** 2026-05-23
**Infrastructure:** GitHub Actions (GitHub-hosted)
**Severity:** Low — workaround is fast and lossless; no data loss, no incorrect
output, no CI false-positive
**Recurrence:** Sporadic — not reproducible on demand; observed once in this
project's history as of filing date

### Symptom

A pull request is opened against `main`. The GitHub PR merge status page shows
all required status checks as "Expected — Waiting for status to be reported"
indefinitely. `gh run list --branch <branch-name>` returns empty — no CI run
has been queued or started. The checks are not skipped; they have simply never
been triggered.

### Trigger condition

Unknown. The condition is not reproducible on demand. The `pull_request` workflow
trigger (`on: pull_request: branches: [main]`) failed to fire when a PR was
opened via `gh pr create`. All other PRs opened in the same session triggered
CI normally.

First observed on PR #481 (a `SESSION_STATE.md`-only PR opened 2026-05-23).
All previous PRs in the session triggered CI without issue.

### Workaround

Push an empty retriggering commit to the branch:

```bash
git commit --allow-empty -m "chore: retrigger CI — empty commit (GH Actions pull_request event did not fire)"
git push origin <branch-name>
```

This triggers the `pull_request` event for the existing PR. CI starts within
seconds. No content changes are needed.

### Impact on SESSION_STATE.md auto-merge

The `auto-merge SESSION_STATE.md` workflow depends on CI triggering. If the
`pull_request` event fails to fire, the PR will hang with all checks "Waiting."
The `gh pr merge --admin` bypass also fails in this state ("5 of 5 required
status checks are expected") because GitHub requires checks to have been
reported before admin bypass is permitted.

The retriggering commit resolves both: once CI fires, the auto-merge workflow
runs and merges the PR without further intervention.

### Upstream

No upstream issue filed. Sporadic GitHub Actions event delivery failures are a
known class of GitHub infrastructure issues. Filing an upstream report is
appropriate if the symptom recurs consistently (three or more times).

---

## Registry Maintenance

### When to file a Known Issue

File a Known Issue when:
- The same external infrastructure problem recurs, OR
- A new external limitation is encountered that required a non-obvious workaround
  to resolve

Do not file a Known Issue for:
- One-time external outages (HTTP 5xx from GitHub, etc.) that resolved without
  a workaround
- Problems that turn out to have an internal root cause (file as a near-miss)

### Entry template

```markdown
## KI-NNN — [Infrastructure]: [Short description]

**Date first observed:** YYYY-MM-DD
**Infrastructure:** [Service or tooling name]
**Severity:** [Low / Medium / High] — [one-line consequence]
**Recurrence:** [Sporadic / Consistent / Resolved]

### Symptom

[What the engineer sees when the issue occurs.]

### Trigger condition

[What causes it, if known. "Unknown" is acceptable.]

### Workaround

[Step-by-step resolution. Include exact commands where relevant.]

### Upstream

[Whether an upstream issue has been filed, and the link if so.]
```

### Severity levels

| Level | Meaning |
|---|---|
| Low | Workaround is quick; no data loss; development continues with minor delay |
| Medium | Workaround exists but requires significant effort; blocks a PR or session |
| High | No reliable workaround; blocks a release or causes incorrect output |

### Recurrence field

| Value | Meaning |
|---|---|
| Sporadic | Observed rarely; not reproducible on demand |
| Consistent | Reproducible; occurs predictably under known conditions |
| Resolved | Upstream fixed; workaround no longer needed (keep entry for historical record) |
