"""add content column to posts table

Revision ID: a994b189278d
Revises: c01b3f816e04
Create Date: 2024-02-05 14:49:56.717298

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a994b189278d'
down_revision: Union[str, None] = 'c01b3f816e04'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('content', sa.String(), nullable=False),
    )


def downgrade() -> None:
    op.drop_column("posts", "content")
