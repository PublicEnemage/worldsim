"""tombstone git_commit_hash — Issue #139 Layer 1 (ADR-004 Decision 1 Amendment)

Revision ID: c7f4a3e9d2b1
Revises: b3c9f2d1a7e5
Create Date: 2026-05-10

Adds git_commit_hash TEXT (nullable) to scenario_deleted_tombstones.

engine_version stores a human-readable semantic version string ("0.3.0") which
is a declaration, not a verifiable pointer — it cannot be resolved to a specific
engine artifact without an external convention. git_commit_hash provides the
precise, unambiguous pointer: a git SHA-1 that identifies the exact engine state
at tombstone write time.

Nullable because tombstones written before this migration have no hash stored.
check_reconstruction_compatibility() in app/api/scenarios.py treats a NULL hash
as "hash not available" and falls back to semantic version comparison only.

Layer 2 (Docker artifact convention for on-demand engine instantiation) is
formally deferred to Milestone 9 — see ADR-004 Decision 1 Amendment.
"""
from __future__ import annotations

import sqlalchemy as sa

from alembic import op

revision = "c7f4a3e9d2b1"
down_revision = "b3c9f2d1a7e5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "scenario_deleted_tombstones",
        sa.Column("git_commit_hash", sa.Text(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("scenario_deleted_tombstones", "git_commit_hash")
