"""create all tables

Revision ID: 9044c17a5905
Revises: 
Create Date: 2024-07-14 21:05:19.925319

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "9044c17a5905"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "meme_templates",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("title", sa.VARCHAR(length=100), nullable=False),
        sa.Column("category", sa.VARCHAR(length=100), nullable=False),
        sa.Column("path", sa.VARCHAR(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_meme_templates")),
    )


    op.create_table(
        "users",
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("username", sa.VARCHAR(length=32), nullable=False),
        sa.Column("email", sa.VARCHAR(), nullable=False),
        sa.Column("hashed_password", sa.LargeBinary(), nullable=False),
        sa.Column(
            "active",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.Enum("admin", "enjoyer", "banned", name="status_enum"),
            server_default="enjoyer",
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(
        op.f("ix_users_username"), "users", ["username"], unique=True
    )


    op.create_table(
        "refresh_sessions",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("refresh_token", sa.VARCHAR(), nullable=False),
        sa.Column("expires_in", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_refresh_sessions_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_refresh_sessions")),
    )
    op.create_index(
        op.f("ix_refresh_sessions_refresh_token"),
        "refresh_sessions",
        ["refresh_token"],
        unique=False,
    )


    op.create_table(
        "telegram_users",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("tg_id", sa.Integer(), nullable=False),
        sa.Column("user_email", sa.VARCHAR(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_email"],
            ["users.email"],
            name=op.f("fk_telegram_users_user_email_users"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_telegram_users")),
        sa.UniqueConstraint("tg_id", name=op.f("uq_telegram_users_tg_id")),
        sa.UniqueConstraint(
            "user_email", name=op.f("uq_telegram_users_user_email")
        ),
    )


    op.create_table(
        "user_meme_templates",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("title", sa.VARCHAR(length=100), nullable=False),
        sa.Column("category", sa.VARCHAR(length=100), nullable=False),
        sa.Column("path", sa.VARCHAR(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_user_meme_templates_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user_meme_templates")),
    )


def downgrade() -> None:
    op.drop_table("user_meme_templates")
    op.drop_table("telegram_users")
    op.drop_index(
        op.f("ix_refresh_sessions_refresh_token"),
        table_name="refresh_sessions",
    )
    op.drop_table("refresh_sessions")
    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
    op.drop_table("meme_templates")
