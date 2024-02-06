"""add user table

Revision ID: e0ef7100c587
Revises: a994b189278d
Create Date: 2024-02-05 14:54:55.850469

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e0ef7100c587'
down_revision: Union[str, None] = 'a994b189278d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("created", sa.TIMESTAMP(timezone=True), 
                  server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email")
    )


def downgrade() -> None:
    op.drop_table("users")
