"""add foriegn key to posts table

Revision ID: ec86976f7393
Revises: e0ef7100c587
Create Date: 2024-02-05 15:07:53.819467

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ec86976f7393'
down_revision: Union[str, None] = 'e0ef7100c587'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("owner_id", sa.Integer(), nullable=False)),
    op.create_foreign_key("post_users_fk", source_table="posts", referent_table="users", local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")
    


def downgrade() -> None:
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column("posts", 'owner_id')
    
