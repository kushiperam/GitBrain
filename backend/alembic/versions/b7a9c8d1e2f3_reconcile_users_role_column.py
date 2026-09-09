"""reconcile users role column

Revision ID: b7a9c8d1e2f3
Revises: 08ffb3a4177e
Create Date: 2026-09-09
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b7a9c8d1e2f3"
down_revision: Union[str, Sequence[str], None] = "08ffb3a4177e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add the missing role column without altering existing user data."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "users" not in inspector.get_table_names():
        raise RuntimeError("Cannot reconcile role: the users table does not exist")

    columns = {column["name"] for column in inspector.get_columns("users")}
    if "role" in columns:
        return

    op.add_column(
        "users",
        sa.Column(
            "role",
            sa.String(length=50),
            nullable=True,
            server_default="developer",
        ),
    )

    if "is_admin" in columns:
        op.execute(
            "UPDATE users "
            "SET role = CASE WHEN is_admin THEN 'admin' ELSE 'developer' END"
        )

    op.alter_column(
        "users",
        "role",
        existing_type=sa.String(length=50),
        nullable=False,
    )


def downgrade() -> None:
    """Intentionally non-destructive: role values must not be discarded."""
    pass
