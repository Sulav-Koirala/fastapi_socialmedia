"""users table

Revision ID: beff4ac9eafd
Revises: 8d8ed0439ed8
Create Date: 2025-07-04 13:27:11.373157

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'beff4ac9eafd'
down_revision: Union[str, Sequence[str], None] = '867244089593'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users",sa.Column("id",sa.Integer(),primary_key=True,nullable=False),
    sa.Column("email",sa.String(),unique=True,nullable=False),
    sa.Column("password",sa.String(),nullable=False),
    sa.Column("created_at",sa.TIMESTAMP(timezone=True),nullable=False, server_default=sa.text('now()')))
    pass

def downgrade() -> None:
    op.drop_table("users")
    pass
