"""add local repository support

Revision ID: ccd41c8f9647
Revises: b7a9c8d1e2f3
Create Date: 2026-09-24

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ccd41c8f9647"
down_revision: Union[str, Sequence[str], None] = "b7a9c8d1e2f3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "repositories",
        sa.Column(
            "source_type",
            sa.String(),
            nullable=False,
            server_default="github",
        ),
    )

    op.add_column(
        "repositories",
        sa.Column(
            "local_path",
            sa.String(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("repositories", "local_path")
    op.drop_column("repositories", "source_type")