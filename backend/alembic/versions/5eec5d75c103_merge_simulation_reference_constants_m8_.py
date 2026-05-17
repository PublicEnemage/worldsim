"""merge simulation_reference_constants_m8_seed and tombstone_git_commit_hash heads

Revision ID: 5eec5d75c103
Revises: b3c5d7e9f1a2, c7f4a3e9d2b1
Create Date: 2026-05-16 22:06:45.847359

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5eec5d75c103'
down_revision = ('b3c5d7e9f1a2', 'c7f4a3e9d2b1')
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
