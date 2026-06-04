"""Unit tests for the session recording API — Pillar 1, M11.5.

Tests use a temporary sessions directory to avoid touching backend/sessions/
and to remain isolated from any real session artifacts.
"""
from __future__ import annotations

import json
from typing import TYPE_CHECKING
from unittest.mock import patch

if TYPE_CHECKING:
    from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app


def _minimal_payload(session_id: str = "2026-06-04-persona-1-001") -> dict:  # type: ignore[type-arg]
    return {
        "session_id": session_id,
        "started_at": "2026-06-04T18:00:00+00:00",
        "ended_at": "2026-06-04T18:15:00+00:00",
        "metadata": {
            "app_version": "v0.11.0",
            "git_commit": "abc12345",
            "persona_id": "persona-1",
            "canonical_use_case": "IMF loan evaluation",
            "cold_start": True,
            "viewport_width": 1440,
            "viewport_height": 900,
            "user_agent": "Mozilla/5.0 (test)",
        },
        "events": [
            {"type": 4, "data": {"href": "http://localhost:5173/"}, "timestamp": 1748973600000}
        ],
        "event_count": 1,
        "duration_ms": 900000,
    }


@pytest.fixture()
def client(tmp_path: Path) -> TestClient:
    with patch("app.api.sessions._SESSIONS_DIR", tmp_path):
        yield TestClient(app)


class TestSaveSessionRecording:
    def test_saves_artifact_and_returns_201(self, client: TestClient, tmp_path: Path) -> None:
        with patch("app.api.sessions._SESSIONS_DIR", tmp_path):
            resp = client.post("/api/v1/sessions/recording", json=_minimal_payload())
        assert resp.status_code == 201
        body = resp.json()
        assert body["session_id"] == "2026-06-04-persona-1-001"
        assert "artifact_path" in body

    def test_artifact_written_to_disk(self, client: TestClient, tmp_path: Path) -> None:
        with patch("app.api.sessions._SESSIONS_DIR", tmp_path):
            client.post("/api/v1/sessions/recording", json=_minimal_payload())
        artifact_path = tmp_path / "2026-06-04-persona-1-001.json"
        assert artifact_path.exists()
        data = json.loads(artifact_path.read_text())
        assert data["session_id"] == "2026-06-04-persona-1-001"
        assert data["schema_version"] == "1.0"
        assert data["event_count"] == 1
        assert len(data["events"]) == 1

    def test_conflict_when_session_id_already_exists(
        self, client: TestClient, tmp_path: Path
    ) -> None:
        with patch("app.api.sessions._SESSIONS_DIR", tmp_path):
            client.post("/api/v1/sessions/recording", json=_minimal_payload())
            resp = client.post("/api/v1/sessions/recording", json=_minimal_payload())
        assert resp.status_code == 409

    def test_rejects_invalid_session_id_format(self, client: TestClient) -> None:
        payload = _minimal_payload(session_id="bad id with spaces!")
        resp = client.post("/api/v1/sessions/recording", json=payload)
        assert resp.status_code == 422

    def test_rejects_session_id_starting_with_hyphen(self, client: TestClient) -> None:
        payload = _minimal_payload(session_id="-bad-start")
        resp = client.post("/api/v1/sessions/recording", json=payload)
        assert resp.status_code == 422

    def test_accepts_alphanumeric_only_id(self, client: TestClient, tmp_path: Path) -> None:
        with patch("app.api.sessions._SESSIONS_DIR", tmp_path):
            resp = client.post(
                "/api/v1/sessions/recording", json=_minimal_payload(session_id="session001")
            )
        assert resp.status_code == 201

    def test_metadata_embedded_in_artifact(self, client: TestClient, tmp_path: Path) -> None:
        with patch("app.api.sessions._SESSIONS_DIR", tmp_path):
            client.post("/api/v1/sessions/recording", json=_minimal_payload())
        data = json.loads((tmp_path / "2026-06-04-persona-1-001.json").read_text())
        assert data["metadata"]["persona_id"] == "persona-1"
        assert data["metadata"]["cold_start"] is True
        assert data["metadata"]["viewport_width"] == 1440


class TestGetSessionRecording:
    def test_retrieves_saved_session(self, client: TestClient, tmp_path: Path) -> None:
        with patch("app.api.sessions._SESSIONS_DIR", tmp_path):
            client.post("/api/v1/sessions/recording", json=_minimal_payload())
            resp = client.get("/api/v1/sessions/recording/2026-06-04-persona-1-001")
        assert resp.status_code == 200
        data = resp.json()
        assert data["session_id"] == "2026-06-04-persona-1-001"
        assert data["event_count"] == 1

    def test_returns_404_for_missing_session(self, client: TestClient, tmp_path: Path) -> None:
        with patch("app.api.sessions._SESSIONS_DIR", tmp_path):
            resp = client.get("/api/v1/sessions/recording/nonexistent-session")
        assert resp.status_code == 404

    def test_returns_400_for_invalid_session_id(self, client: TestClient) -> None:
        resp = client.get("/api/v1/sessions/recording/has spaces!")
        assert resp.status_code in (400, 404, 422)


class TestListSessionRecordings:
    def test_returns_empty_list_when_no_sessions(self, client: TestClient, tmp_path: Path) -> None:
        with patch("app.api.sessions._SESSIONS_DIR", tmp_path):
            resp = client.get("/api/v1/sessions/recording")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_lists_saved_sessions(self, client: TestClient, tmp_path: Path) -> None:
        with patch("app.api.sessions._SESSIONS_DIR", tmp_path):
            client.post("/api/v1/sessions/recording", json=_minimal_payload("session-a"))
            client.post("/api/v1/sessions/recording", json=_minimal_payload("session-b"))
            resp = client.get("/api/v1/sessions/recording")
        assert resp.status_code == 200
        ids = [s["session_id"] for s in resp.json()]
        assert "session-a" in ids
        assert "session-b" in ids

    def test_summary_contains_required_fields(self, client: TestClient, tmp_path: Path) -> None:
        with patch("app.api.sessions._SESSIONS_DIR", tmp_path):
            client.post("/api/v1/sessions/recording", json=_minimal_payload())
            resp = client.get("/api/v1/sessions/recording")
        summary = resp.json()[0]
        assert summary["session_id"] == "2026-06-04-persona-1-001"
        assert summary["persona_id"] == "persona-1"
        assert summary["event_count"] == 1
        assert summary["duration_ms"] == 900000

    def test_skips_malformed_json_files(self, client: TestClient, tmp_path: Path) -> None:
        (tmp_path / "corrupt.json").write_text("not json", encoding="utf-8")
        with patch("app.api.sessions._SESSIONS_DIR", tmp_path):
            resp = client.get("/api/v1/sessions/recording")
        assert resp.status_code == 200
