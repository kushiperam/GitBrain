"""rename password to hashed_password

Revision ID: 125cc80fe7d5
Revises: 902fbc7e0e98
Create Date: 2026-08-01 14:08:33.896211

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '125cc80fe7d5'
down_revision: Union[str, Sequence[str], None] = '902fbc7e0e98'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Step 1: Add new hashed_password column temporarily allowing NULL
    op.add_column(
        'users',
        sa.Column(
            'hashed_password',
            sa.String(length=255),
            nullable=True
        )
    )

    # Step 2: Copy existing password values into hashed_password
    op.execute(
        "UPDATE users SET hashed_password = password"
    )

    # Step 3: Make hashed_password NOT NULL
    op.alter_column(
        'users',
        'hashed_password',
        nullable=False
    )

    # Step 4: Remove old password column
    op.drop_column(
        'users',
        'password'
    )


def downgrade() -> None:
    """Downgrade schema."""

    # Restore password column
    op.add_column(
        'users',
        sa.Column(
            'password',
            sa.String(length=255),
            nullable=False
        )
    )

    # Copy hashed passwords back
    op.execute(
        "UPDATE users SET password = hashed_password"
    )

    # Remove hashed_password column
    op.drop_column(
        'users',
        'hashed_password'
    )