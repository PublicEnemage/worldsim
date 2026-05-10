"""Unit tests for tombstone reconstruction version guard — Issue #139 Layer 1.

Tests check_reconstruction_compatibility() and _resolve_git_commit_hash() from
app/api/scenarios.py. No database required — all tests exercise pure logic.

Coverage:
  1. Matching version + matching hash → passes (no exception).
  2. Matching version + NULL tombstone hash → passes (pre-migration tombstone).
  3. Matching version + "unknown" live hash → passes (hash comparison skipped).
  4. Matching version + "unknown" tombstone hash → passes (hash comparison skipped).
  5. Version mismatch → HTTPException(409).
  6. Version match + hash mismatch → HTTPException(409).
  7. Version mismatch + force_audit_override=True → no exception, warning logged.
  8. Hash mismatch + force_audit_override=True → no exception, warning logged.
  9. 409 detail includes both tombstone and live engine_version strings.
  10. 409 detail includes both tombstone and live git_commit_hash values.
  11. _GIT_COMMIT_HASH is a non-empty string (either a hex SHA-1 or "unknown").
  12. _GIT_COMMIT_HASH is either 40-char hex or "unknown" — no other values.
  13. _ENGINE_VERSION is non-empty and matches the expected semver pattern.
"""
from __future__ import annotations

import re

import pytest
from fastapi import HTTPException

from app.api.scenarios import (
    _ENGINE_VERSION,
    _GIT_COMMIT_HASH,
    check_reconstruction_compatibility,
)

# Convenience aliases for the live values — tests that want to assert a "match"
# pass these so they remain correct regardless of which version is deployed.
_LIVE_VERSION = _ENGINE_VERSION
_LIVE_HASH = _GIT_COMMIT_HASH


# ---------------------------------------------------------------------------
# Happy-path: compatible tombstones should not raise
# ---------------------------------------------------------------------------


def test_matching_version_and_hash_passes() -> None:
    """Identical version and hash — reconstruction is safe."""
    check_reconstruction_compatibility(_LIVE_VERSION, _LIVE_HASH)


def test_matching_version_null_hash_passes() -> None:
    """NULL tombstone hash (pre-migration tombstone) — falls back to version only."""
    check_reconstruction_compatibility(_LIVE_VERSION, None)


def test_matching_version_unknown_live_hash_passes() -> None:
    """When live hash is 'unknown', hash comparison is skipped."""
    import unittest.mock as mock

    with mock.patch("app.api.scenarios._GIT_COMMIT_HASH", "unknown"):
        check_reconstruction_compatibility(_LIVE_VERSION, "abc123deadbeef")


def test_matching_version_unknown_tombstone_hash_passes() -> None:
    """When tombstone hash is 'unknown', hash comparison is skipped."""
    check_reconstruction_compatibility(_LIVE_VERSION, "unknown")


def test_matching_version_both_unknown_hash_passes() -> None:
    """Both hashes unknown — version match alone is sufficient."""
    import unittest.mock as mock

    with mock.patch("app.api.scenarios._GIT_COMMIT_HASH", "unknown"):
        check_reconstruction_compatibility(_LIVE_VERSION, "unknown")


# ---------------------------------------------------------------------------
# Version mismatch → HTTPException(409)
# ---------------------------------------------------------------------------


def test_version_mismatch_raises_409() -> None:
    """Different engine_version → reconstruction blocked."""
    with pytest.raises(HTTPException) as exc_info:
        check_reconstruction_compatibility("0.1.0", _LIVE_HASH)
    assert exc_info.value.status_code == 409


def test_version_mismatch_detail_includes_tombstone_version() -> None:
    """409 detail must include the tombstone's engine_version for diagnostics."""
    with pytest.raises(HTTPException) as exc_info:
        check_reconstruction_compatibility("0.1.0", None)
    assert "0.1.0" in exc_info.value.detail


def test_version_mismatch_detail_includes_live_version() -> None:
    """409 detail must include the live engine_version for diagnostics."""
    with pytest.raises(HTTPException) as exc_info:
        check_reconstruction_compatibility("0.1.0", None)
    assert _LIVE_VERSION in exc_info.value.detail


# ---------------------------------------------------------------------------
# Hash mismatch → HTTPException(409)
# ---------------------------------------------------------------------------


def test_hash_mismatch_raises_409() -> None:
    """Matching version but different git hash → reconstruction blocked."""
    import unittest.mock as mock

    with mock.patch("app.api.scenarios._GIT_COMMIT_HASH", "a" * 40), \
            pytest.raises(HTTPException) as exc_info:
        check_reconstruction_compatibility(_LIVE_VERSION, "b" * 40)
    assert exc_info.value.status_code == 409


def test_hash_mismatch_detail_includes_tombstone_hash() -> None:
    """409 detail must include the tombstone git_commit_hash."""
    import unittest.mock as mock

    tombstone_hash = "c" * 40
    with mock.patch("app.api.scenarios._GIT_COMMIT_HASH", "d" * 40), \
            pytest.raises(HTTPException) as exc_info:
        check_reconstruction_compatibility(_LIVE_VERSION, tombstone_hash)
    assert tombstone_hash in exc_info.value.detail


def test_hash_mismatch_detail_includes_live_hash() -> None:
    """409 detail must include the live git_commit_hash."""
    import unittest.mock as mock

    live_hash = "e" * 40
    with mock.patch("app.api.scenarios._GIT_COMMIT_HASH", live_hash), \
            pytest.raises(HTTPException) as exc_info:
        check_reconstruction_compatibility(_LIVE_VERSION, "f" * 40)
    assert live_hash in exc_info.value.detail


# ---------------------------------------------------------------------------
# force_audit_override=True → no raise, warning logged
# ---------------------------------------------------------------------------


def test_version_mismatch_with_audit_override_does_not_raise(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """force_audit_override=True logs a WARNING instead of raising."""
    import logging

    with caplog.at_level(logging.WARNING, logger="app.api.scenarios"):
        check_reconstruction_compatibility(
            "0.1.0", None, force_audit_override=True
        )
    assert any("mismatch" in r.message.lower() for r in caplog.records)


def test_hash_mismatch_with_audit_override_does_not_raise(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """force_audit_override=True suppresses 409 even on hash mismatch."""
    import logging
    import unittest.mock as mock

    with mock.patch("app.api.scenarios._GIT_COMMIT_HASH", "a" * 40), \
            caplog.at_level(logging.WARNING, logger="app.api.scenarios"):
        check_reconstruction_compatibility(
            _LIVE_VERSION, "b" * 40, force_audit_override=True
        )
    assert any("mismatch" in r.message.lower() for r in caplog.records)


def test_matching_version_with_audit_override_does_not_raise_or_warn(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """force_audit_override=True on a compatible tombstone is a no-op."""
    import logging

    with caplog.at_level(logging.WARNING, logger="app.api.scenarios"):
        check_reconstruction_compatibility(_LIVE_VERSION, _LIVE_HASH, force_audit_override=True)
    assert not caplog.records


# ---------------------------------------------------------------------------
# Module-level constants
# ---------------------------------------------------------------------------


def test_git_commit_hash_is_non_empty_string() -> None:
    """_GIT_COMMIT_HASH must always be a non-empty string."""
    assert isinstance(_GIT_COMMIT_HASH, str)
    assert len(_GIT_COMMIT_HASH) > 0


def test_git_commit_hash_is_hex_sha1_or_unknown() -> None:
    """_GIT_COMMIT_HASH is either a 40-char hex SHA-1 or the sentinel 'unknown'."""
    assert _GIT_COMMIT_HASH == "unknown" or re.fullmatch(r"[0-9a-f]{40}", _GIT_COMMIT_HASH), (
        f"_GIT_COMMIT_HASH has unexpected format: {_GIT_COMMIT_HASH!r}"
    )


def test_engine_version_is_non_empty() -> None:
    """_ENGINE_VERSION must be a non-empty string."""
    assert isinstance(_ENGINE_VERSION, str)
    assert len(_ENGINE_VERSION) > 0


def test_engine_version_matches_semver_pattern() -> None:
    """_ENGINE_VERSION must follow MAJOR.MINOR.PATCH semver format."""
    assert re.fullmatch(r"\d+\.\d+\.\d+", _ENGINE_VERSION), (
        f"_ENGINE_VERSION does not match semver: {_ENGINE_VERSION!r}"
    )
