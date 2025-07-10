"""create products table

Revision ID: bdfaad1ebe51
Revises: 
Create Date: 2025-07-08 17:21:31.892182

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bdfaad1ebe51'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'products',
        sa.Column('product_id', sa.Integer, primary_key=True),
        sa.Column('product_name', sa.Unicode(100), nullable=False),
        sa.Column('description', sa.Unicode(200)),
        sa.Column('specs', sa.JSON),
        sa.Column('price', sa.Float),
        sa.Column('stock_quantity', sa.Integer, nullable=False)
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('products')    
