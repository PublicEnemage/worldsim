# Pillar 3 — Session Provenance Standard

**Milestone 11.5 — Usability Validation and Experience Audit**

| | |
|---|---|
| Authors | Data Architect Agent (§2–4), PM Agent (§1, §5) |
| Consulted | Frontend Architect Agent (component naming), UX Designer Agent (zone classification) |
| Status | ESTABLISHED — effective for all M11.5 sessions |
| Issue | #719 |
| Version | 1.0 (2026-06-04) |

---

## §1 — Purpose (PM Agent)

A usability finding is empirical evidence. For findings to be comparable across sessions,
versions, and agents, every session must be precisely documented at the moment it runs —
not reconstructed afterward.

This standard governs the provenance record for every Pillar 2 usability session. It
specifies:

- The session manifest schema (§2) — what is recorded and when
- The linking protocol (§3) — how the five session artifacts are connected
- The versioning strategy (§4) — how the standard tracks application changes
- The manifest directory and naming convention (§5)

The **semantic component vocabulary** is maintained as a companion document:
`docs/ux/usability-sessions/vocabulary.md`

Both documents must be established before any Pillar 2 session runs. This document
establishes the standard; the vocabulary is the reference the standard names.

---

## §2 — Session Manifest Schema (Data Architect Agent)

The session manifest is a Markdown document filled in by the coordinator before the
session begins (static fields) and immediately after it ends (outcome fields). It is
the human-readable provenance record — not a substitute for the machine-generated
interaction trace, but the document that makes the trace interpretable six months
from now by an agent who was not present.

### 2.1 Schema

```yaml
# Session manifest — Pillar 3 provenance record
# Standard version: 1.0
# File: docs/ux/usability-sessions/manifests/<session_id>-manifest.md

session_id: "<YYYY-MM-DD-persona-N-NNN>"
manifest_version: "1.0"

## Application state

app_version: "<e.g. v0.11.0>"
git_commit: "<8-char SHA — from git rev-parse --short HEAD>"
active_modules:
  - "<e.g. EcologicalModule>"
  - "<e.g. GovernanceModule>"
  - "<e.g. PoliticalEconomyModule>"
active_fixtures:
  - "<e.g. greece_2010_2015>"
  - "<e.g. argentina_2001_2002>"

## Agent configuration

agent_id: "<e.g. claude-sonnet-4-6>"
persona_id: "<e.g. persona-2>"
persona_name: "<e.g. Finance Ministry Negotiator — Eleni Papadopoulos>"
canonical_use_case: "<e.g. IMF loan evaluation>"
task_prompt_version: "pillar-2-methodology.md §Appendix A / Persona 2 / v1.0"
cold_start: true
orientation_provided: "<verbatim description of any briefing given beyond the task prompt, or 'none'>"

## Environmental conditions

viewport_width: <integer — CSS pixels>
viewport_height: <integer — CSS pixels>
browser: "<user agent string>"
frontend_url: "http://localhost:5173"
backend_url: "http://localhost:8000"
session_url: "http://localhost:5173/?usability_session=<session_id>&persona=<persona_id>&use_case=<use_case>"

## Session timing

session_started_at: "<ISO8601 UTC — from rrweb artifact started_at>"
session_ended_at: "<ISO8601 UTC — from rrweb artifact ended_at>"
duration_ms: <integer — from rrweb artifact duration_ms>
ended_by: "<agent | coordinator | time-limit>"

## Outcome (completed after session)

task_completed: <true | false | partial>
concluded_marker_present: <true | false>
think_aloud_markers_count:
  LOOKING_FOR: <integer>
  EXPECTED: <integer>
  FOUND: <integer>
  CONFUSED: <integer>
  GAVE_UP_ON: <integer>
  TRIED: <integer>
  CONCLUDED: <integer>
session_valid: <true | false>
invalidity_reason: "<if session_valid is false, state the reason>"

## Artifact links

interaction_trace: "backend/sessions/<session_id>.json"
transcript: "docs/ux/usability-sessions/transcripts/<session_id>-transcript.md"
field_notes: "docs/ux/usability-sessions/transcripts/<session_id>-field-notes.md"
findings: "docs/ux/usability-sessions/findings/<session_id>-findings.md"
```

### 2.2 Field notes

**`active_modules`** — List every module that was enabled in the running backend at
session time. Check `backend/app/api/scenarios.py` or the scenario configuration for
the modules instantiated. If the session used a pre-built fixture (Greece, Argentina),
list the modules enabled in that fixture's `build_*_scenario()` function.

**`git_commit`** — Run `git rev-parse --short HEAD` on the running frontend/backend
at session time. Both should match; if they differ, record both.

**`cold_start`** — Always `true` for M11.5 sessions. A session where the agent was
given any description of WorldSim's interface, layout, or features before navigation
began is not a valid cold-start session and must be recorded as invalid.

**`ended_by`** — `agent` if the agent clicked End Session; `coordinator` if the
coordinator clicked it after the agent emitted `[CONCLUDED: ...]`; `time-limit` if
the 45-minute limit was reached.

**`session_valid`** — A session is valid if all three conditions hold: (1) the
interaction trace exists and is non-empty, (2) the think-aloud transcript contains
at least one each of `[LOOKING FOR:]`, (`[FOUND:]` or `[CONFUSED:]`), and `[CONCLUDED:]`,
(3) coordinator field notes are written. A session that fails any condition is recorded
as invalid; it may be re-run with a new session ID.

---

## §3 — Linking Protocol (Data Architect Agent)

The `session_id` is the primary key connecting all five session artifacts. It is
assigned by the coordinator before the session begins and appears in every artifact's
filename and content.

### 3.1 Artifact map

| Artifact | Path | Author | Created |
|---|---|---|---|
| Interaction trace | `backend/sessions/<session_id>.json` | Pillar 1 (rrweb) | Automatically on End Session |
| Think-aloud transcript | `docs/ux/usability-sessions/transcripts/<session_id>-transcript.md` | Agent | During session |
| Coordinator field notes | `docs/ux/usability-sessions/transcripts/<session_id>-field-notes.md` | Coordinator | Immediately after session |
| Findings document | `docs/ux/usability-sessions/findings/<session_id>-findings.md` | UX Designer + PM | Within 48h of session |
| Session manifest | `docs/ux/usability-sessions/manifests/<session_id>-manifest.md` | Coordinator | Before + immediately after session |

### 3.2 Cross-reference rule

Every finding in the findings document must cite its source session_id. The session_id
appears in the finding header (see Pillar 2 methodology §8 finding format). This is the
chain that makes a finding traceable: finding → session_id → manifest → all four other
artifacts.

A finding without a session_id citation is not a valid finding.

### 3.3 Vocabulary reference

Every finding that locates a failure in a specific UI component must use the canonical
vocabulary term from `vocabulary.md`. The vocabulary term appears in the finding's
`Component:` field. A finding that uses a non-canonical component reference (e.g.,
"the alert panel" instead of `zone-1b / alert-row`) cannot be reliably linked to
future sessions running against a changed component.

---

## §4 — Versioning Strategy (Data Architect Agent)

### 4.1 This standard

The standard version is recorded in every manifest (`manifest_version`). When a
breaking change is made to the manifest schema (a required field is added, renamed,
or removed), the standard version is bumped and the change is logged in §4.3.

Additive changes (a new optional field is added) do not require a version bump but
must be logged.

### 4.2 The semantic component vocabulary

The vocabulary document (`vocabulary.md`) carries its own version. Every session
manifest records the vocabulary version in use at session time as part of the
application state record — this is implicit in the `git_commit` field, since the
vocabulary is versioned alongside the application. If the vocabulary version cannot
be derived from the git commit (e.g., a manual session run outside the normal
workflow), the coordinator records it explicitly in the `task_prompt_version` field.

When a UI component is added, renamed, or removed:

- **Added component** — add to vocabulary, log in §Changelog of `vocabulary.md`,
  no version bump required
- **Renamed component** — update vocabulary entry, mark old name as deprecated with
  a `→` pointer to the new name, bump vocabulary minor version, log in §Changelog
- **Removed component** — remove vocabulary entry, mark as `[REMOVED vX.Y]`, bump
  vocabulary minor version, log in §Changelog

The vocabulary update must be in the same PR as the component change. Schema drift
between the live application and the vocabulary is a compliance violation equivalent
to API contract drift.

### 4.3 Changelog

| Date | Standard version | Change |
|---|---|---|
| 2026-06-04 | 1.0 | Initial standard established (Issue #719) |

---

## §5 — Manifest Directory and Naming Convention (PM Agent)

Manifests are stored at:

```
docs/ux/usability-sessions/manifests/<session_id>-manifest.md
```

The directory is created alongside this standard. Session manifests are committed to
the repository as the session runs — they are not ephemeral notes. A manifest that
exists only locally is not a valid provenance record.

The `session_id` in the filename must exactly match the `session_id` in the Pillar 1
rrweb artifact filename (`backend/sessions/<session_id>.json`) and the `usability_session`
URL parameter used to initiate the session. Any mismatch between these three is a
linking failure and must be corrected before the findings document is written.

---

## §6 — Relation to Pillar 1 Artifact (Data Architect Agent)

The Pillar 1 session artifact (`backend/sessions/<session_id>.json`, schema version 1.0)
already captures a subset of what this standard requires: `app_version`, `git_commit`,
`persona_id`, `canonical_use_case`, `cold_start`, `viewport_width`, `viewport_height`,
`user_agent`, `started_at`, `ended_at`, `duration_ms`.

The session manifest does not duplicate these fields — it references the interaction
trace artifact as the authoritative source for machine-generated fields. The manifest
adds what the Pillar 1 artifact cannot capture: active modules, active fixtures,
agent_id, task_prompt version, ended_by, outcome fields, and the full artifact link map.

The schema comment in `docs/schema/session_recording.yml` previously anticipated a
`manifest_id` field linking the recording to a future manifest standard. That linkage
is now established through the `session_id` — no new field is required, and the
recording schema remains at version 1.0. The `session_recording.yml` comment has been
updated to reflect this resolution.
