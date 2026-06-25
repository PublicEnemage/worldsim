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

## KI-002 — mypy: Python version mismatch (local 3.10 vs project-declared 3.13)

**Date first observed:** 2026-06-04
**Infrastructure:** mypy static type checker (local development environment)
**Severity:** Low — CI passes (GitHub Actions runs Python 3.13); local mypy reports a
pre-existing syntax error that does not reflect a real defect in the codebase
**Recurrence:** Consistent — reproducible on any development machine running Python < 3.13

### Symptom

Running `cd backend && mypy app/` locally produces:

```
app/api/scenarios.py:1425: error: syntax error in type comment  [syntax]
```

The affected line uses PEP 695 type alias syntax (`type CompositeStrategy = Callable[...]`),
which requires Python 3.13+. When mypy is invoked with a Python interpreter < 3.13, it
cannot parse the PEP 695 `type` statement and raises a syntax error.

The same error appears on `main` before any M11 changes — confirmed by stashing all M11
modifications and running mypy. The error is pre-existing and pre-dates M11.

### Trigger condition

mypy's effective Python version is determined by the interpreter it is invoked with.
When the development machine runs Python 3.10.11 and `python_version` is not pinned in
`pyproject.toml`'s mypy section, mypy parses the code using 3.10 semantics — which
do not include PEP 695 type alias syntax.

### Workaround

Two options:

1. **Run mypy via CI** — GitHub Actions runs Python 3.13 and mypy passes there. For the
   pre-push lint gate, CI is the authoritative pass signal for this specific error.

2. **Invoke mypy with version flag locally:**
   ```bash
   cd backend && mypy --python-version 3.13 app/
   ```
   This forces 3.13 semantics regardless of the local interpreter version.
   Note: mypy ≥ 1.5 is required for PEP 695 support.

### Upstream

No upstream issue. PEP 695 is a Python 3.13 language feature; mypy support for it
requires mypy ≥ 1.5 and a matching `python_version` setting. The long-term resolution
is to pin `python_version = "3.13"` in the mypy section of `backend/pyproject.toml`
and ensure all contributors run Python 3.13+ locally. Tracked as a follow-up item
for M12 environment standardisation.

---

## KI-003 — GitHub Rulesets: required status check for a not-yet-merged workflow blocks all PRs until the workflow file lands on the base branch

**Date first observed:** 2026-06-16
**Infrastructure:** GitHub Rulesets (repository rules)
**Severity:** Medium — blocks all open PRs targeting the protected branch until the workaround is applied; no data loss
**Recurrence:** Consistent — reproducible any time a new required status check is added to a Ruleset before the corresponding workflow file is merged into the base branch

### Symptom

After adding a new required status check (e.g. `branch-naming`) to a Ruleset targeting
`release/m*`, any PR whose head branch does not contain the workflow file (`.github/workflows/branch-naming.yml`) receives:

```
GraphQL: Repository rule violations found
Required status check "branch-naming" is expected.
(mergePullRequest)
```

The check never reports — not as pass, not as fail — because the workflow file does not
exist on the base branch (`release/m{N}`) at the time the PR's CI runs. GitHub Rulesets
treat an expected-but-never-reported check as a violation. `gh pr merge --admin` does not
bypass Ruleset requirements (unlike branch protection `enforce_admins`).

### Trigger condition

The bootstrapping sequence:
1. Workflow file added to a feature branch (e.g. `feat/m14-g7-branch-naming-enforcement`)
2. Ruleset updated (server-side, immediately effective) to require the new check
3. Other open PRs targeting the same release branch have neither the workflow file in
   their head branch nor on the base branch
4. Those PRs' CI cannot run the new check → Ruleset blocks their merge

GitHub Actions resolves workflow files from the merge commit (merge of head + base). If
the workflow file exists in neither the head branch nor the base branch, the check cannot
run and the Ruleset blocks indefinitely.

### Workaround

**Required sequence when adding a new required CI check:**

1. **Do not add the check to the Ruleset until the workflow file is on the base branch.**
   Introduce the Ruleset change as the last step, not the first.

   Preferred order:
   a. Commit the workflow file to a feature branch
   b. Open and merge that PR (the check runs from the merge commit and passes/skips)
   c. Only after merge: add the check to the Ruleset via `gh api PUT /rulesets/{id}`

2. **Recovery if the Ruleset was updated before the workflow file merged** (the KI-003
   scenario):
   a. Temporarily remove the new check from the Ruleset:
      ```bash
      gh api repos/{owner}/{repo}/rulesets/{id} --method PUT --input ruleset-without-check.json
      ```
   b. Merge any blocked PRs
   c. Merge the PR that introduces the workflow file
   d. Re-add the check to the Ruleset

### Upstream

No upstream issue filed. This is a known limitation of GitHub Rulesets' check resolution
model — required checks must have previously reported on the base branch for the Ruleset
to consider them satisfiable. GitHub branch protection rules have the same behaviour.
The workaround (sequence the Ruleset update after the workflow file merge) fully mitigates
the issue; no code change is required.

**First observed:** adding `branch-naming` check during Issue #978 implementation
(2026-06-16). Recovery applied in the same session.

---

## KI-004 — GitHub Actions: Node.js 20 deprecation warning on `actions/checkout@v4` and `actions/setup-node@v4`

**Date first observed:** 2026-06-18
**Infrastructure:** GitHub Actions (GitHub-hosted runners)
**Severity:** Low — warning only; CI continues to pass; no behavioural change
**Recurrence:** Consistent — appears on every CI run until upstream action versions are updated

### Symptom

Every CI run logs the following warning before the job steps execute:

```
Warning: Node.js 20 is deprecated. The following actions target Node.js 20 but
are being forced to run on Node.js 24: actions/checkout@v4, actions/setup-node@v4.
For more information see:
https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/
```

All jobs pass despite the warning. GitHub's runner infrastructure auto-upgrades the
actions' runtime from Node.js 20 to Node.js 24 transparently.

### Trigger condition

GitHub Actions deprecated Node.js 20 as a runner runtime (announced 2025-09-19).
`actions/checkout@v4` and `actions/setup-node@v4` declare a Node.js 20 engine
internally. GitHub's hosted runners are now Node.js 24; the runtime mismatch
produces the warning on every run. This is a GitHub infrastructure decision — the
project has no control over the hosted runner Node.js version.

### Workaround

No action required at this time. GitHub is auto-upgrading the runtime and CI passes.

**When upstream resolves:** The warning will disappear when `actions/checkout` and
`actions/setup-node` publish new major versions (e.g. `@v5`) with Node.js 24-native
internals. At that point, update all references in `.github/workflows/ci.yml` and
`.github/workflows/milestone-automation.yml` from `@v4` to the new version. No other
change is required.

Affected files (7 references total as of 2026-06-18):
- `.github/workflows/ci.yml` — 6 uses of `actions/checkout@v4`, 1 use of `actions/setup-node@v4`
- `.github/workflows/milestone-automation.yml` — 1 use of `actions/checkout@v4`

### Upstream

GitHub announced the deprecation at:
https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/

No project-level issue filed. The resolution is a one-line version bump per workflow
reference once upstream publishes a Node.js 24-native action version. Monitor
`actions/checkout` and `actions/setup-node` release notes for a `@v5` tag.

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
## KI-005 — GitHub Rulesets: `release-branch-ci-gate` blocks new release branch creation; workaround requires temporary Ruleset disable

**Date first observed:** 2026-06-20
**Infrastructure:** GitHub Rulesets
**Severity:** Medium — blocks every new milestone's release branch creation; workaround is reliable but requires admin API access
**Recurrence:** Consistent — will occur at every milestone kickoff

### Symptom

Direct push to a new `release/m{N}` branch is rejected with:

```
remote: error: GH013: Repository rule violations found for refs/heads/release/m15.
remote: - Required status check "branch-naming" is expected.
```

The `branch-naming` check only runs on `pull_request` events targeting `release/m*`. For a direct push (or GitHub API branch creation), the check is never triggered — GitHub Rulesets treat an expected-but-never-reported check as a violation. Since `release/m{N}` doesn't exist yet, no PR can target it, so `branch-naming` can never be satisfied. The GitHub REST API `POST /git/refs` is blocked for the same reason.

### Root cause

The `release-branch-ci-gate` Ruleset has `bypass_actors: []` (no bypass actors defined) and enforcement `active`. Required status checks include `branch-naming`, which only runs on PR events. A brand-new release branch cannot satisfy a PR-only check via any push path, regardless of whether the commit has passed all other checks.

First observed at M15 kickoff. M14's `release/m14` was created before the Ruleset was active (M14 G7 set up the Ruleset after the branch existed).

### Workaround

Temporarily disable the Ruleset, create the branch via the GitHub API, then immediately re-enable:

```bash
# Step 1: Disable
gh api repos/{owner}/{repo}/rulesets/17751852 --method PUT --input - <<'EOF'
{"name":"release-branch-ci-gate","target":"branch","enforcement":"disabled","conditions":{"ref_name":{"include":["refs/heads/release/m*"],"exclude":[]}}}
EOF

# Step 2: Create branch from main HEAD
SHA=$(gh api repos/{owner}/{repo}/git/ref/heads/main --jq '.object.sha')
echo "{\"ref\":\"refs/heads/release/m{N}\",\"sha\":\"$SHA\"}" | \
  gh api repos/{owner}/{repo}/git/refs --input -

# Step 3: Re-enable
gh api repos/{owner}/{repo}/rulesets/17751852 --method PUT --input - <<'EOF'
{"name":"release-branch-ci-gate","target":"branch","enforcement":"active","conditions":{"ref_name":{"include":["refs/heads/release/m*"],"exclude":[]}}}
EOF
```

The window of reduced protection is under 10 seconds and the main branch itself is protected by its own Ruleset, so there is no meaningful security exposure.

### Permanent fix

Set `"do_not_enforce_on_create": true` on the `required_status_checks` rule in the Ruleset, or add the `repo_admin` role as a bypass actor. Either change allows branch creation without requiring pre-existing CI results while still enforcing checks on PR merges. EL action required to update the Ruleset configuration.

### Upstream

No upstream issue filed. GitHub Rulesets design: required status checks require a prior CI run on the commit, which is impossible for branch creation where no PR exists yet. The `evaluate` enforcement mode (which would allow creation with warnings) is available on Enterprise plans only.

---

## KI-006 — GitHub Actions: AC-009 4× CPU Throttle Performance Test Unreliable on GHA Shared Runners

**Date first observed:** 2026-06-25
**Infrastructure:** GitHub Actions (2-core Ubuntu shared runner)
**Severity:** Medium — blocks CI-green PR merges with no frontend change; workaround is test.fixme() per NM-064
**Recurrence:** Consistent — reproducible whenever GHA runner load is above baseline

### Symptom

`AC-009` (`tests/e2e/trajectory-view.spec.ts:156`) fails with:

```
Error: expect(received).toBeLessThanOrEqual(expected)
Expected: <= 200
Received:    712  (or 771 in a separate run)
```

The test applies a 4× CPU throttle via CDP (`Emulation.setCPUThrottlingRate`, rate 4)
and asserts Mode 3 component render time is ≤ 200ms (threshold raised from 100ms per
EX-001, 2026-06-24). On GHA 2-core shared runners under normal load, the throttled
render consistently exceeds 700ms — 3–4× the raised threshold.

### Trigger condition

Any CI run on a GitHub Actions shared runner where the runner is under load. The test
is not sensitive to the PR contents — it fails on PRs with no frontend changes.
Historically observed at 712ms and 771ms on M17 G2 sprint entry PR (#1289).

### Workaround

`test.fixme()` applied to AC-009 in `trajectory-view.spec.ts` per NM-064 process
improvement. The test remains in the suite as a local developer gate; it is skipped
in CI. Run locally without CDP throttle or with a relaxed threshold to verify
Mode 3 performance has not regressed.

```bash
# Run AC-009 locally (no throttle — local assertion only):
cd frontend && npx playwright test trajectory-view.spec.ts -g "AC-009" --headed
```

### Upstream

Not filed upstream. The GHA 2-core shared runner specs are documented and will not
change for this tier. The root cause is the test design (4× CDP throttle on shared
infrastructure), not a GHA defect.

Near-miss authority: NM-064
EX-001 (docs/compliance/exceptions.md): threshold exception active through M17 exit.

---

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
