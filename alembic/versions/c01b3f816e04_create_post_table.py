"""create post table

Revision ID: c01b3f816e04
Revises: 
Create Date: 2024-02-05 14:36:49.542205

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c01b3f816e04'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(), nullable=False),
    )



def downgrade() -> None:
    op.drop_table('posts')

# class Post(Base):
#     __tablename__ = "posts"

#     id = Column(Integer, primary_key=True, nullable=False)
#     title = Column(String, nullable=False)
#     content = Column(String, nullable=False)
#     published = Column(Boolean, nullable=False, server_default='TRUE')
#     created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
#     owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)


#     # relationship to help fetch extra information from the database
#     owner = relationship("User")