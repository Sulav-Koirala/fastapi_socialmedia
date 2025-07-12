"""fk to posts

Revision ID: 6261408ea15f
Revises: 69e564599544
Create Date: 2025-07-04 14:02:14.500404

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6261408ea15f'
down_revision: Union[str, Sequence[str], None] = '867244089593'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",
    sa.Column("user_id",sa.Integer(),nullable=False)
    )
    op.create_foreign_key("posts_users_fk",source_table="posts",referent_table="users",local_cols=["user_id"],remote_cols=["id"],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("posts_users_fk",table_name="posts")
    op.drop_column("posts","user_id")
    pass
