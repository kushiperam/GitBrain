"""add role to users

Revision ID: d2ecfa5c06e6
Revises: 125cc80fe7d5
Create Date: 2026-08-01 16:00:07.519792

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d2ecfa5c06e6"
down_revision: Union[str, Sequence[str], None] = "125cc80fe7d5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "users",
        sa.Column(
            "role",
            sa.String(length=50),
            nullable=False,
            server_default="developer",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("users", "role")