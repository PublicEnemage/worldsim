"""Session recording API — Pillar 1, M11.5 usability audit.

Endpoints store and retrieve rrweb session recording artifacts as local JSON
files in backend/sessions/. No session data leaves the local machine.

Activation: frontend records when ?usability_session=<id> is in the URL.
Recordings are saved by calling POST /sessions/recording when the session ends.
"""
from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, field_validator

router = APIRouter(prefix="/sessions", tags=["sessions"])

_SESSIONS_DIR = Path(__file__).parents[3] / "sessions"
_SESSION_ID_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}$")


def _sessions_dir() -> Path:
    _SESSIONS_DIR.mkdir(exist_ok=True)
    return _SESSIONS_DIR


class SessionMetadata(BaseModel):
    app_version: str
    git_commit: str
    persona_id: str
    canonical_use_case: str
    cold_start: bool
    viewport_width: int
    viewport_height: int
    user_agent: str


class SessionRecordingPayload(BaseModel):
    session_id: str
    started_at: str
    ended_at: str
    metadata: SessionMetadata
    events: list[Any]
    event_count: int
    duration_ms: int

    @field_validator("session_id")
    @classmethod
    def validate_session_id(cls, v: str) -> str:
        if not _SESSION_ID_RE.match(v):
            raise ValueError(
                "session_id must be 1–64 characters, start with alphanumeric, "
                "and contain only alphanumeric, hyphens, and underscores"
            )
        return v


class SavedSessionResponse(BaseModel):
    session_id: str
    artifact_path: str


class SessionSummary(BaseModel):
    session_id: str
    created_at: str
    persona_id: str
    canonical_use_case: str
    event_count: int
    duration_ms: int


@router.post(
    "/recording",
    response_model=SavedSessionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def save_session_recording(
    payload: SessionRecordingPayload,
) -> SavedSessionResponse:
    """Save a usability session recording artifact to disk."""
    path = _sessions_dir() / f"{payload.session_id}.json"
    if path.exists():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Session '{payload.session_id}' already exists.",
        )
    artifact: dict[str, Any] = {
        "schema_version": "1.0",
        "session_id": payload.session_id,
        "created_at": datetime.now(UTC).isoformat(),
        "started_at": payload.started_at,
        "ended_at": payload.ended_at,
        "metadata": payload.metadata.model_dump(),
        "events": payload.events,
        "event_count": payload.event_count,
        "duration_ms": payload.duration_ms,
    }
    path.write_text(json.dumps(artifact, ensure_ascii=False, indent=2), encoding="utf-8")
    return SavedSessionResponse(
        session_id=payload.session_id,
        artifact_path=str(path.resolve()),
    )


@router.get("/recording/{session_id}")
async def get_session_recording(session_id: str) -> dict[str, Any]:
    """Retrieve a stored session recording artifact."""
    if not _SESSION_ID_RE.match(session_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid session ID format.",
        )
    path = _sessions_dir() / f"{session_id}.json"
    if not path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session '{session_id}' not found.",
        )
    return json.loads(path.read_text(encoding="utf-8"))  # type: ignore[no-any-return]


@router.get("/recording", response_model=list[SessionSummary])
async def list_session_recordings() -> list[SessionSummary]:
    """List all available session recording artifacts."""
    sessions_dir = _sessions_dir()
    summaries: list[SessionSummary] = []
    for path in sorted(sessions_dir.glob("*.json")):
        try:
            data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
            meta: dict[str, Any] = data.get("metadata", {})
            summaries.append(
                SessionSummary(
                    session_id=data["session_id"],
                    created_at=data.get("created_at", ""),
                    persona_id=meta.get("persona_id", ""),
                    canonical_use_case=meta.get("canonical_use_case", ""),
                    event_count=data.get("event_count", 0),
                    duration_ms=data.get("duration_ms", 0),
                )
            )
        except (KeyError, json.JSONDecodeError, ValueError):
            continue
    return summaries
