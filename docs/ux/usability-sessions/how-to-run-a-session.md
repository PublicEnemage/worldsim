# How to Run a Usability Session — M11.5 Pillar 1

This document is the coordinator's guide for running a Pillar 2 usability session
using the Pillar 1 instrumentation layer. Read it before starting any session.

## Prerequisites

- WorldSim backend running: `cd backend && uvicorn app.main:app --reload`
- WorldSim frontend running: `cd frontend && npm run dev`
- Both must be up before the session URL is opened

## Step 1 — Assign a session ID

Choose a session ID that identifies the persona, date, and sequence:

```
2026-06-04-persona-1-001
```

Format: `YYYY-MM-DD-<persona-id>-<sequence>` (alphanumeric, hyphens, underscores only).
The session ID becomes the artifact filename. Make it human-readable.

## Step 2 — Construct the session URL

```
http://localhost:5173/?usability_session=<session_id>&persona=<persona_id>&use_case=<use_case_label>
```

Example:
```
http://localhost:5173/?usability_session=2026-06-04-persona-1-001&persona=persona-1&use_case=IMF+loan+evaluation
```

URL parameters:
- `usability_session` — **required** — enables recording and sets the session ID
- `persona` — optional — links the artifact to the persona (e.g. `persona-1`)
- `use_case` — optional — labels the canonical use case (URL-encoded spaces as `+`)

Without `usability_session`, recording is completely disabled and the application
behaves identically to normal use. There is no accidental recording.

## Step 3 — Send the URL to the agent

Give the agent exactly this URL. Do not brief them on WorldSim's architecture,
navigation, or features. The session must be a cold start — no orientation.

Give the agent their role context and the question they need to answer. Nothing else.

## Step 4 — During the session

A red banner appears at the top of the viewport showing:
```
● Recording: 2026-06-04-persona-1-001     [End Session]
```

This confirms recording is active. The agent navigates normally.

The coordinator should be watching (screen share or in-person) and noting the
think-aloud markers from the agent (see Pillar 2 protocol when established).

### Coordinator communication gate (NM-033)

If the agent asks the coordinator a direct question during the session, the coordinator
must **stop and classify the question before responding:**

> **Is this about agent-visible WorldSim context (forbidden), or operational mechanics (allowed)?**

- **Agent-visible WorldSim context** (navigation hints, feature location, what a panel means,
  whether the agent is on the right track) — respond only with: *"I can't help with that —
  navigate as you would if you were alone."* Never answer, even partially.
- **Operational mechanics** (is the tool running, is the URL correct, is there a technical error)
  — you may answer factually without revealing anything about WorldSim's architecture or content.

This gate exists because Session 003 (NM-033) showed that a coordinator answering what
appeared to be a neutral question ("is the tool working?") can seed enough context to
break the cold-start condition. When in doubt, treat the question as agent-visible context
and refuse. The cost of a false positive is one unanswered question; the cost of a false
negative is an invalid session.

## Step 5 — End the session

The agent (or coordinator) clicks **End Session** in the red banner.

The banner turns green and shows:
```
● Session saved: 2026-06-04-persona-1-001
  Artifact written to backend/sessions/ — you may close this tab.
```

The artifact is now at `backend/sessions/2026-06-04-persona-1-001.json`.

## Step 6 — Verify the artifact

```bash
# List all saved sessions
curl http://localhost:8000/api/v1/sessions/recording

# Retrieve a specific session summary
curl http://localhost:8000/api/v1/sessions/recording/2026-06-04-persona-1-001 | python3 -m json.tool | head -20
```

## Step 7 — Replay the session

Open in a browser:
```
http://localhost:5173/?replay_session=2026-06-04-persona-1-001
```

The replay viewer loads the session artifact from the backend and plays it back
using rrweb. Press **▶ Play** to start. The replay runs in an iframe at the
original viewport dimensions.

The replay viewer only shows when `?replay_session=` is in the URL. It is not
a user-facing feature.

## Session artifact schema

`docs/schema/session_recording.yml` — session JSON structure, field definitions,
and linkage to the Pillar 3 session provenance standard (Issue #719).

## Troubleshooting

**Red banner does not appear:**
- Confirm `usability_session` is in the URL (not `session` or `recording_session`)
- Confirm the frontend is running on port 5173

**End Session shows "Save failed":**
- Confirm the backend is running on port 8000
- A session with this ID may already exist — choose a new session ID

**Replay shows "not found":**
- Confirm the backend is running
- Confirm the session was saved (End Session turned green)
- Check `backend/sessions/` for the artifact file
