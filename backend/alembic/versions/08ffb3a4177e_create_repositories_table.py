"""create repositories table

Revision ID: 08ffb3a4177e
Revises: d2ecfa5c06e6
Create Date: 2026-08-01 19:47:11.148005
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "08ffb3a4177e"
down_revision: Union[str, Sequence[str], None] = "d2ecfa5c06e6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "repositories",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("url", sa.String(), nullable=False),
        sa.Column("owner_id", sa.Integer(), sa.ForeignKey("users.id")),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
        ),
    )

    op.create_index(
        "ix_repositories_id",
        "repositories",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_repositories_id",
        table_name="repositories",
    )

    op.drop_table("repositories")