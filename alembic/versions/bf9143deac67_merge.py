"""merge

Revision ID: bf9143deac67
Revises: 434daccd2e9c, beff4ac9eafd
Create Date: 2025-07-04 14:23:20.381744

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bf9143deac67'
down_revision: Union[str, Sequence[str], None] = ('434daccd2e9c', 'beff4ac9eafd')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
