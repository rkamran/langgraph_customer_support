"""create troubleshooting_guides table

Revision ID: 2cf90ee33026
Revises: d0353874387b
Create Date: 2025-07-08 17:46:26.512875

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2cf90ee33026'
down_revision: Union[str, Sequence[str], None] = 'd0353874387b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'troubleshooting_guides',
        sa.Column('guide_id', sa.Integer, primary_key=True),
        sa.Column('product_category', sa.Unicode(100), nullable=False),
        sa.Column('issue_description', sa.Unicode(1024)),
        sa.Column('solution_steps', sa.Unicode(2048)),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('troubleshooting_guides')    
