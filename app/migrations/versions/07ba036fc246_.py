"""empty message

Revision ID: 07ba036fc246
Revises: a902b2e85586
Create Date: 2025-02-15 14:10:13.836145

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = "07ba036fc246"
down_revision: Union[str, None] = "a902b2e85586"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "userstable",
        sa.Column(
            "bio", sqlmodel.sql.sqltypes.AutoString(length=1500), nullable=True
        ),
        sa.Column("email", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_superuser", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column(
            "password_hash", sqlmodel.sql.sqltypes.AutoString(), nullable=False
        ),
        sa.Column(
            "username", sqlmodel.sql.sqltypes.AutoString(), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_userstable_username"),
        "userstable",
        ["username"],
        unique=False,
    )
    op.drop_index("ix_users_table_email", table_name="users_table")
    op.drop_index("ix_users_table_username", table_name="users_table")
    op.drop_table("users_table")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users_table",
        sa.Column("id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column(
            "username",
            sa.VARCHAR(length=50),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "password_hash", sa.TEXT(), autoincrement=False, nullable=False
        ),
        sa.Column("bio", sa.TEXT(), autoincrement=False, nullable=True),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "email", sa.VARCHAR(length=50), autoincrement=False, nullable=False
        ),
        sa.Column(
            "is_activated", sa.BOOLEAN(), autoincrement=False, nullable=False
        ),
        sa.PrimaryKeyConstraint("id", name="users_table_pkey"),
        sa.UniqueConstraint("id", name="users_table_id_key"),
    )
    op.create_index(
        "ix_users_table_username", "users_table", ["username"], unique=True
    )
    op.create_index(
        "ix_users_table_email", "users_table", ["email"], unique=True
    )
    op.drop_index(op.f("ix_userstable_username"), table_name="userstable")
    op.drop_table("userstable")
    # ### end Alembic commands ###
