"""post table

Revision ID: 867244089593
Revises: 
Create Date: 2025-07-04 12:58:41.791592

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '867244089593'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("posts",sa.Column("id",sa.Integer(),primary_key=True,nullable=False),
    sa.Column("title",sa.String(),nullable=False),
    sa.Column("content",sa.String(),nullable=False),
    sa.Column("rating",sa.Integer(), nullable=True),
    sa.Column("post",sa.Boolean(),nullable=False,server_default='TRUE'),
    sa.Column("created_at",sa.TIMESTAMP(timezone=True),nullable=False, server_default=sa.text('now()'))
    )
    pass
    
def downgrade() -> None:
    op.drop_table("posts")
    pass