"""create orders table

Revision ID: d0353874387b
Revises: bdfaad1ebe51
Create Date: 2025-07-08 17:37:08.170918

"""
from os import name
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd0353874387b'
down_revision: Union[str, Sequence[str], None] = 'bdfaad1ebe51'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'orders',
        sa.Column('order_id', sa.Integer, primary_key=True),
        sa.Column('customer_id', sa.Integer, nullable=False),
        sa.Column('order_date', sa.DateTime),
        sa.Column('status', sa.Enum('Processing', 'Shipped', 'Delivered', name="order_status"), nullable=False),
        sa.Column('tracking_number', sa.String(100))
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('orders')
