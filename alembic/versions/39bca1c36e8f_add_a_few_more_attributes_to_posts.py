"""add a few more attributes to posts

Revision ID: 39bca1c36e8f
Revises: ec86976f7393
Create Date: 2024-02-05 15:18:31.433098

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '39bca1c36e8f'
down_revision: Union[str, None] = 'ec86976f7393'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column("published", sa.Boolean(), nullable=False, server_default='True'),)
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=True, server_default=sa.text('now()')),)


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
