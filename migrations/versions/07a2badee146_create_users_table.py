"""create users table

Revision ID: 07a2badee146
Revises: d5539ec11ca9
Create Date: 2026-06-19 15:46:54.845608

"""

from datetime import datetime, timezone
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "07a2badee146"
down_revision: Union[str, Sequence[str], None] = "d5539ec11ca9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "api_users",
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column(
            "is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("username"),
    )
    op.create_index(
        op.f("ix_api_users_username"), "api_users", ["username"], unique=True
    )

    # Insert seeds (reemplaza los hashed_password por los que generaste)
    api_users_table = sa.table(
        "api_users",
        sa.column("username", sa.String),
        sa.column("hashed_password", sa.String),
        sa.column("is_active", sa.Boolean),
        sa.column("created_at", sa.DateTime),
    )
    now = datetime.now(timezone.utc)
    op.bulk_insert(
        api_users_table,
        [
            {
                "username": "admin",
                "hashed_password": "$2b$12$gFJZuFyATUZuzf9/jKoDkOniFpy0yfQ7X0Xt4s1IZjgoYkhYAnqA.",
                "is_active": True,
                "created_at": now,
            },
            {
                "username": "usuario",
                "hashed_password": "$2b$12$coeVIpaFqgN1cJZ9qxEDGelWBGDKEz2/ciFiQXt0B8hrrUqjcLcMW",
                "is_active": True,
                "created_at": now,
            },
        ],
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    op.drop_index(op.f("ix_api_users_username"), table_name="api_users")
    op.execute("DROP TABLE api_users CASCADE;")


# ### end Alembic commands ###
