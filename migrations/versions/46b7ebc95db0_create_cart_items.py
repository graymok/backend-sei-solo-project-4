"""create-cart_items

Revision ID: 46b7ebc95db0
Revises: d61a4280502f
Create Date: 2021-05-21 13:48:55.857152

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46b7ebc95db0'
down_revision = 'd61a4280502f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'cart_items',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer),
        sa.Column('order_id', sa.Integer),
        sa.Column('product_id', sa.Integer),
        sa.Column('is_ordered', sa.Boolean),            
    )


def downgrade():
    op.drop_table('cart_items')
